import pandas as pd
import numpy as np
import scipy
import scipy.stats
import psycopg2

query = """SELECT COUNT(*) 
FROM posts as p, postLinks as pl, postHistory as ph, votes as v, badges as b, users as u 
WHERE p.Id = pl.RelatedPostId 
  AND u.Id = p.OwnerUserId 
  AND u.Id = b.UserId 
  AND u.Id = ph.UserId 
  AND u.Id = v.UserId 
AND p.CommentCount>=0 AND p.CommentCount<=13 
AND ph.PostHistoryTypeId=5 AND ph.CreationDate<='2014-08-13 09:20:10'::timestamp
AND v.CreationDate>='2010-07-19 00:00:00'::timestamp 
AND b.Date<='2014-09-09 10:24:35'::timestamp 
AND u.Views>=0 AND u.DownVotes>=0 AND u.CreationDate>='2010-08-04 16:59:53'::timestamp AND u.CreationDate<='2014-07-22 15:15:22'::timestamp;"""

def prepare_date(sample_size):
    u = pd.read_csv("datasets/stats_blocked/users.csv")
    u = u[['id', 'pageid', 'views', 'creationdate', 'downvotes']]
    p = pd.read_csv("datasets/stats_blocked/posts.csv")
    p = p[['id', 'pageid', 'owneruserid', 'commentcount']]
    b = pd.read_csv("datasets/stats_blocked/badges.csv")
    b = b[['userid', 'date']]
    v = pd.read_csv("datasets/stats_blocked/votes.csv")
    v = v[['userid', 'creationdate']]
    pl = pd.read_csv("datasets/stats_blocked/postLinks.csv")
    pl = pl[['relatedpostid']]
    ph = pd.read_csv("datasets/stats_blocked/postHistory.csv")
    ph = ph[['userid', 'posthistorytypeid', 'creationdate']]


    u["creationdate"] = pd.to_datetime(u["creationdate"])
    b["date"] = pd.to_datetime(b["date"])
    ph['creationdate'] = pd.to_datetime(ph['creationdate'])
    v['creationdate'] = pd.to_datetime(v['creationdate'])

    u_page_ids = u["pageid"].unique()
    p_page_ids = p["pageid"].unique()

    u_sample_page_ids = np.random.choice(u_page_ids, sample_size, replace=True)
    p_sample_page_ids = np.random.choice(p_page_ids, sample_size, replace=True)

    u_sample = u[u["pageid"].isin(u_sample_page_ids)]
    p_sample = p[p["pageid"].isin(p_sample_page_ids)]

    sample_rate_u = sample_size / len(u_page_ids)
    sample_rate_p = sample_size / len(p_page_ids)

    return u, p, b, v, pl, ph, u_sample, p_sample, sample_rate_u, sample_rate_p

def more_sample(table: pd.DataFrame, sample_size: int, original_sample: pd.DataFrame):
    page_ids = table["pageid"].unique()
    sample_page_ids = np.random.choice(page_ids, sample_size, replace=True)
    new_sample = table[table["pageid"].isin(sample_page_ids)]
    return pd.concat([original_sample, new_sample])

def filter_u(u):
    return u[(u["views"] >= 0) & (u["downvotes"] >= 0) 
             & (u["creationdate"] >= pd.Timestamp("2010-08-04 16:59:53"))
             & (u["creationdate"] <= pd.Timestamp("2014-07-22 15:15:22"))]

def filter_b(b):
    return b[b["date"] <= pd.Timestamp("2014-09-09 10:24:35")]

def filter_v(v):
    return v[(v["creationdate"] >= pd.Timestamp("2010-07-19 00:00:00"))]

def filter_ph(ph):
    return ph[(ph["posthistorytypeid"] == 5) & (ph["creationdate"] <= pd.Timestamp("2014-08-13 09:20:10"))]

def filter_p(p):
    return p[(p["commentcount"] >= 0) & (p["commentcount"] <= 13)]

def join(left_t, right_t, left_key, right_key, left_suffix, right_suffix):
    return pd.merge(left_t, right_t, 
                    left_on=left_key, right_on=right_key, 
                    how="inner", suffixes=(left_suffix, right_suffix))

def estimate(u_sample: pd.DataFrame, p_sample: pd.DataFrame, p: pd.DataFrame, 
             b: pd.DataFrame, v: pd.DataFrame, pl: pd.DataFrame, 
             ph: pd.DataFrame, sample_rate_u, sample_rate_p):
    # apply filter
    u_sample_filtered = filter_u(u_sample)
    p_sample_filtered = filter_p(p_sample)
    p_filtered = filter_p(p)
    b_filtered = filter_b(b)
    v_filtered = filter_v(v)
    ph_filtered = filter_ph(ph)

    p.drop(columns=["pageid"], inplace=True)

    # apply sub joins
    pl_pf = join(p_sample_filtered, pl, "id", "relatedpostid", "_p", "_pl")
    print("done pl_pf", len(pl_pf))

    pf_u = join(p_filtered, u_sample, "owneruserid", "id", "_p", "_u")
    phf_pf_u = join(ph_filtered, pf_u, "userid", "id_u", "_ph", "_p")
    print("done phf_pf_u", len(phf_pf_u))

    vf_pf_u = join(v_filtered, pf_u, "userid", "id_u", "_v", "_p")
    print("done vf_pf_u", len(vf_pf_u))

    bf_pf_u = join(b_filtered, pf_u, "userid", "id_u", "_b", "_p")
    print("done bf_pf_u", len(bf_pf_u))

    uf_pf = join(u_sample_filtered, p_filtered, "id", "owneruserid", "_u", "_p")
    print("done uf_pf", len(uf_pf))

    phf_u = join(ph_filtered, u_sample, "userid", "id", "_ph", "_u")
    vf_phf_u = join(v_filtered, phf_u, "userid", "id", "_v", "_ph")
    print("done vf_phf_u", len(vf_phf_u))

    bf_phf_u = join(b_filtered, phf_u, "userid", "id", "_b", "_ph")
    print("done bf_phf_u", len(bf_phf_u))

    uf_phf = join(u_sample_filtered, ph_filtered, "id", "userid", "_u", "_ph")
    print("done uf_phf", len(uf_phf))

    vf_u = join(v_filtered, u_sample, "userid", "id", "_v", "_u")
    bf_vf_u = join(b_filtered, vf_u, "userid", "id", "_b", "_v")
    print("done bf_vf_u", len(bf_vf_u))

    uf_vf = join(u_sample_filtered, v_filtered, "id", "userid", "_u", "_v")
    print("done uf_vf", len(uf_vf))

    uf_bf = join(u_sample_filtered, b_filtered, "id", "userid", "_u", "_b")
    print("done uf_bf", len(uf_bf))

    phf_pf_pl_u = join(phf_pf_u, pl, "id_p", "relatedpostid", "_ph", "_pl")
    print("done phf_pf_pl_u", len(phf_pf_pl_u))

    vf_pf_pl_u = join(vf_pf_u, pl, "id_p", "relatedpostid", "_v", "_pl")
    print("done vf_pf_pl_u", len(vf_pf_pl_u))

    bf_pf_pl_u = join(bf_pf_u, pl, "id_p", "relatedpostid", "_b", "_pl")
    print("done bf_pf_pl_u", len(bf_pf_pl_u))

    uf_pf_pl = join(uf_pf, pl, "id_p", "relatedpostid", "_p", "_pl")
    print("done uf_pf_pl", len(uf_pf_pl))

    vf_pf_phf_u = join(vf_pf_u, ph_filtered, "id_u", "userid", "_v", "_ph")
    print("done vf_pf_phf_u", len(vf_pf_phf_u))

    bf_pf_phf_u = join(bf_pf_u, ph_filtered, "id_u", "userid", "_b", "_ph")
    print("done bf_pf_phf_u", len(bf_pf_phf_u))

    uf_pf_phf = join(uf_pf, ph_filtered, "id_u", "userid", "_p", "_ph")
    print("done uf_pf_phf", len(uf_pf_phf))

    bf_pf_v_u = join(bf_pf_u, vf_u, "id_u", "userid", "_b", "_v")
    print("done bf_pf_v_u", len(bf_pf_v_u))

    uf_pf_vf = join(uf_pf, v_filtered, "id_u", "userid", "_p", "_v")
    print("done uf_pf_vf", len(uf_pf_vf))

    uf_pf_bf = join(uf_pf, b_filtered, "id_u", "userid", "_p", "_b")
    print("done uf_pf_bf", len(uf_pf_bf))

    bf_phf_vf_u = join(bf_phf_u, v_filtered, "id", "userid", "_b", "_v")
    print("done bf_phf_vf_u", len(bf_phf_vf_u))

    uf_phf_vf = join(uf_phf, v_filtered, "id", "userid", "_ph", "_v")
    print("done uf_phf_vf", len(uf_phf_vf))

    uf_phf_bf = join(uf_phf, b_filtered, "id", "userid", "_ph", "_b")
    print("done uf_phf_bf", len(uf_phf_bf))

    uf_vf_bf = join(uf_vf, b_filtered, "id", "userid", "_v", "_b")
    print("done uf_vf_bf", len(uf_vf_bf))

    vf_pf_pl_phf_u = join(vf_pf_pl_u, ph_filtered, "id_u", "userid", "_pl", "_ph")
    print("done vf_pf_pl_phf_u", len(vf_pf_pl_phf_u))

    bf_pf_pl_phf_u = join(bf_pf_pl_u, ph_filtered, "id_u", "userid", "_pl", "_ph")
    print("done bf_pf_pl_phf_u", len(bf_pf_pl_phf_u))

    uf_pf_pl_phf = join(uf_pf_pl, ph_filtered, "id_u", "userid", "_pl", "_ph")
    print("done uf_pf_pl_phf", len(uf_pf_pl_phf))

    bf_pf_pl_vf_u = join(bf_pf_pl_u, v_filtered, "id_u", "userid", "_pl", "_v")
    print("done bf_pf_pl_vf_u", len(bf_pf_pl_vf_u))

    uf_pf_pl_vf = join(uf_pf_pl, v_filtered, "id_u", "userid", "_pl", "_v")
    print("done uf_pf_pl_vf", len(uf_pf_pl_vf))

    uf_pf_pl_bf = join(uf_pf_pl, b_filtered, "id_u", "userid", "_pl", "_b")
    print("done uf_pf_pl_bf", len(uf_pf_pl_bf))

    bf_pf_phf_vf_u = join(bf_pf_phf_u, v_filtered, "id_u", "userid", "_ph", "_v")
    print("done bf_pf_phf_vf_u", len(bf_pf_phf_vf_u))

    uf_pf_phf_vf = join(uf_pf_phf, v_filtered, "id_u", "userid", "_ph", "_v")
    print("done uf_pf_phf_vf", len(uf_pf_phf_vf))

    uf_pf_phf_bf = join(uf_pf_phf, b_filtered, "id_u", "userid", "_ph", "_b")
    print("done uf_pf_phf_bf", len(uf_pf_phf_bf))

    uf_pf_vf_bf = join(uf_pf_vf, b_filtered, "id_u", "userid", "_v", "_b")
    print("done uf_pf_vf_bf", len(uf_pf_vf_bf))

    uf_phf_vf_bf = join(uf_phf_vf, b_filtered, "id", "userid", "_v", "_b")
    print("done uf_phf_vf_bf", len(uf_phf_vf_bf))

    bf_pf_pl_phf_vf_u = join(bf_pf_pl_phf_u, v_filtered, "id_u", "userid", "_pl", "_v")
    print("done bf_pf_pl_phf_vf_u", len(bf_pf_pl_phf_vf_u))

    uf_pf_pl_phf_vf = join(uf_pf_pl_phf, v_filtered, "id_u", "userid", "_pl", "_v")
    print("done uf_pf_pl_phf_vf", len(uf_pf_pl_phf_vf))

    uf_pf_pl_phf_bf = join(uf_pf_pl_phf, b_filtered, "id_u", "userid", "_pl", "_b")
    print("done uf_pf_pl_phf_bf", len(uf_pf_pl_phf_bf))

    uf_pf_pl_vf_bf = join(uf_pf_pl_vf, b_filtered, "id_u", "userid", "_pl", "_b")
    print("done uf_pf_pl_vf_bf", len(uf_pf_pl_vf_bf))

    uf_pf_phf_vf_bf = join(uf_pf_phf_vf, b_filtered, "id_u", "userid", "_ph", "_b")
    print("done uf_pf_phf_vf_bf", len(uf_pf_phf_vf_bf))

    uf_pf_pl_phf_vf_bf = join(uf_pf_pl_phf_vf, b_filtered, "id_u", "userid", "_pl", "_b")
    print("done uf_pf_pl_phf_vf_bf", len(uf_pf_pl_phf_vf_bf))

    subjoins = [pl_pf, phf_pf_u, vf_pf_u, bf_pf_u, uf_pf, vf_phf_u, bf_phf_u,
                uf_phf, bf_vf_u, uf_vf, uf_bf, phf_pf_pl_u, vf_pf_pl_u, bf_pf_pl_u,
                uf_pf_pl, vf_pf_phf_u, bf_pf_phf_u, uf_pf_phf, bf_pf_v_u, uf_pf_vf,
                uf_pf_bf, bf_phf_vf_u, uf_phf_vf, uf_phf_bf, uf_vf_bf, vf_pf_pl_phf_u,
                bf_pf_pl_phf_u, uf_pf_pl_phf, bf_pf_pl_vf_u, uf_pf_pl_vf, uf_pf_pl_bf,
                bf_pf_phf_vf_u, uf_pf_phf_vf, uf_pf_phf_bf, uf_pf_vf_bf, uf_phf_vf_bf,
                bf_pf_pl_phf_vf_u, uf_pf_pl_phf_vf, uf_pf_pl_phf_bf, uf_pf_pl_vf_bf,
                uf_pf_phf_vf_bf, uf_pf_pl_phf_vf_bf]
    
    for subjoin in subjoins:
        print(len(subjoin))
    
    lbs = []
    ubs = []
    ests = []
    
    for i, subjoin in enumerate(subjoins):
        if i == 0:
            sample_rate = sample_rate_p
        else:
            sample_rate = sample_rate_u

        est = len(subjoin) / sample_rate
        ests.append(est)

        for col in subjoin.columns:
            if col == "pageid":
                continue
            r_col = col
        subjoin_blocked_count = subjoin.groupby("pageid")[r_col].count()
        n_block = len(subjoin_blocked_count)
        block_mean = subjoin_blocked_count.mean()
        block_std = subjoin_blocked_count.std()
        z = scipy.stats.norm.ppf(0.975)
        block_mean_lb = block_mean - z * block_std / np.sqrt(n_block)
        block_mean_ub = block_mean + z * block_std / np.sqrt(n_block)

        lb = max(block_mean_lb * n_block / sample_rate, 0)
        ub = block_mean_ub * n_block / sample_rate

        lbs.append(lb)
        ubs.append(ub)
    
    return lbs, ubs, ests

def explain(lbs, ubs, ests):
    reward = []
    for i in range(len(lbs)):
        new_ests_lb = ests[:i] + [lbs[i]] + ests[i+1:]
        with open("stats_db/tmp_57.txt", "w") as f:
            for est in new_ests_lb:
                f.write(str(est) + "\n")

        with psycopg2.connect("dbname=stats user=yuxuan18") as conn:
            with conn.cursor() as cur:
                setup = "SET ml_joinest_enabled=true; SET query_no=0; SET join_est_no=0; SET ml_joinest_fname='tmp_57.txt';"
                cur.execute(f"{setup} EXPLAIN {query}")
                lb_plan = cur.fetchall()

        new_ests_ub = ests[:i] + [ubs[i]] + ests[i+1:]
        with open("stats_db/tmp_56.txt", "w") as f:
            for est in new_ests_lb:
                f.write(str(est) + "\n")

        with psycopg2.connect("dbname=stats user=yuxuan18") as conn:
            with conn.cursor() as cur:
                setup = "SET ml_joinest_enabled=true; SET query_no=0; SET join_est_no=0; SET ml_joinest_fname='tmp_57.txt';"
                cur.execute(f"{setup} EXPLAIN {query}")
                ub_plan = cur.fetchall()

        is_same = compare_plans(postprocess_plan(lb_plan), postprocess_plan(ub_plan))
        reward.append(is_same)
    return reward
    
def postprocess_plan(plan):
    for i, op in enumerate(plan):
        end_pos = op[0].find("(cost")
        if end_pos != -1:
            plan[i] = op[0][:end_pos]
        else:
            plan[i] = op[0]
    return plan

def compare_plans(lb_plan, ub_plan):
    for i in range(min(len(lb_plan), len(ub_plan))):
        if lb_plan[i] != ub_plan[i]:
            return False
    return True


sample_size = 50
u, p, b, v, pl, ph, u_sample, p_sample, sample_rate_u, sample_rate_p = prepare_date(sample_size)
lbs, ubs, ests = estimate(u_sample, p_sample, p, b, v, pl, ph, sample_rate_u, sample_rate_p)
reward = explain(lbs, ubs, ests)
print(reward)
