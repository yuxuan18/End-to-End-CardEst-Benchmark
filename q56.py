import pandas as pd
import numpy as np
import scipy
import scipy.stats
import psycopg2

query = """SELECT COUNT(*) 
FROM tags as t, posts as p, users as u, votes as v, badges as b 
WHERE p.Id = t.ExcerptPostId 
  AND u.Id = v.UserId 
  AND u.Id = b.UserId 
  AND u.Id = p.OwnerUserId 
  AND u.Views>=0 AND u.Views<=515 AND u.UpVotes>=0 AND u.CreationDate<='2014-09-07 13:46:41'::timestamp 
  AND v.BountyAmount>=0 AND v.BountyAmount<=200 
  AND b.Date<='2014-09-12 12:56:22'::timestamp;"""

def prepare_date(sample_size):
    u = pd.read_csv("datasets/stats_blocked/users.csv")
    u = u[['id', 'pageid', 'views', 'upvotes', 'creationdate']]
    p = pd.read_csv("datasets/stats_blocked/posts.csv")
    p = p[['id', 'pageid', 'owneruserid']]
    t = pd.read_csv("datasets/stats_blocked/tags.csv")
    t = t[['excerptpostid']]
    b = pd.read_csv("datasets/stats_blocked/badges.csv")
    b = b[['userid', 'date']]
    v = pd.read_csv("datasets/stats_blocked/votes.csv")
    v = v[['userid', 'bountyamount']]

    u["creationdate"] = pd.to_datetime(u["creationdate"])
    b["date"] = pd.to_datetime(b["date"])

    u_page_ids = u["pageid"].unique()
    p_page_ids = p["pageid"].unique()

    u_sample_page_ids = np.random.choice(u_page_ids, sample_size, replace=True)
    p_sample_page_ids = np.random.choice(p_page_ids, sample_size, replace=True)

    u_sample = u[u["pageid"].isin(u_sample_page_ids)]
    p_sample = p[p["pageid"].isin(p_sample_page_ids)]

    sample_rate_u = sample_size / len(u_page_ids)
    sample_rate_p = sample_size / len(p_page_ids)

    return u, p, t, b, v, u_sample, p_sample, sample_rate_u, sample_rate_p

def more_sample(table: pd.DataFrame, sample_size: int, original_sample: pd.DataFrame):
    page_ids = table["pageid"].unique()
    sample_page_ids = np.random.choice(page_ids, sample_size, replace=True)
    new_sample = table[table["pageid"].isin(sample_page_ids)]
    return pd.concat([original_sample, new_sample])

def filter_u(u):
    return u[(u["views"] >= 0) & (u["views"] <= 515) 
             & (u["upvotes"] >= 0) & (u["creationdate"] <= pd.Timestamp("2014-09-07 13:46:41"))]

def filter_b(b):
    return b[b["date"] <= pd.Timestamp("2014-09-12 12:56:22")]

def filter_v(v):
    return v[(v["bountyamount"] >= 0) & (v["bountyamount"] <= 200)]

def join(left_t, right_t, left_key, right_key, left_suffix, right_suffix):
    return pd.merge(left_t, right_t, 
                    left_on=left_key, right_on=right_key, 
                    how="inner", suffixes=(left_suffix, right_suffix))

def estimate(u_sample, p_sample, p: pd.DataFrame, t, b, v, sample_rate_u, sample_rate_p):
    # apply filter
    u_sample_filtered = filter_u(u_sample)
    b_filtered = filter_b(b)
    v_filtered = filter_v(v)
    p.drop(columns=["pageid"], inplace=True)

    # apply sub joins
    p_t = join(p_sample, t, "id", "excerptpostid", "_p", "_t")

    uf_p = join(u_sample_filtered, p, "id", "owneruserid", "_u", "_p")
    
    u_p = join(u_sample, p, "id", "owneruserid", "_u", "_p")
    u_p_vf = join(u_p, v_filtered, "id_u", "userid", "_p", "_v")

    u_p_b = join(u_p, b, "id_u", "userid", "_p", "_b")

    uf_vf = join(u_sample_filtered, v_filtered, "id", "userid", "_u", "_v")

    uf_bf = join(u_sample_filtered, b_filtered, "id", "userid", "_u", "_b")

    u_vf = join(u_sample, v_filtered, "id", "userid", "_u", "_v")
    u_vf_bf = join(u_vf, b_filtered, "id", "userid", "_v", "_b")

    uf_p_t = join(uf_p, t, "id_p", "excerptpostid", "_p", "_t")

    u_p_t = join(u_p, t, "id_p", "excerptpostid", "_p", "_t")
    u_p_t_vf = join(u_p_t, v_filtered, "id_u", "userid", "_t", "_v")

    u_p_t_bf = join(u_p_t, b_filtered, "id_u", "userid", "_t", "_b")
    
    uf_p_vf = join(uf_p, v_filtered, "id_u", "userid", "_p", "_v")

    uf_bf_p = join(uf_bf, p, "id", "owneruserid", "_b", "_p")

    u_p_bf = join(u_p, b_filtered, "id_u", "userid", "_p", "_b")
    u_bf_p_vf = join(u_p_bf, v_filtered, "id_u", "userid", "_p", "_v")

    uf_bf_vf = join(uf_bf, v_filtered, "id", "userid", "_b", "_v")

    uf_p_t_vf = join(uf_p_t, v_filtered, "id_u", "userid", "_t", "_v")

    uf_p_t_bf = join(uf_p_t, b_filtered, "id_u", "userid", "_t", "_b")

    u_p_t_bf_vf = join(u_p_t_bf, v_filtered, "id_u", "userid", "_b", "_v")

    uf_bf_p_vf = join(uf_bf_p, v_filtered, "id_b", "userid", "_p", "_v")

    uf_bf_p_vf_t = join(uf_bf_p_vf, t, "id_p", "excerptpostid", "_v", "_t")

    subjoins = [p_t, uf_p, u_p_vf, u_p_b, uf_vf, uf_bf, 
                u_vf_bf, uf_p_t, u_p_t_vf, u_p_t_bf, 
                uf_p_vf, uf_bf_p, u_bf_p_vf, uf_bf_vf, uf_p_t_vf, 
                uf_p_t_bf, u_p_t_bf_vf, uf_bf_p_vf, uf_bf_p_vf_t]
    
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
        with open("/mydata/stats_db/tmp_56.txt", "w") as f:
            for est in new_ests_lb:
                f.write(str(est) + "\n")

        with psycopg2.connect("dbname=stats user=yuxuan18") as conn:
            with conn.cursor() as cur:
                setup = "SET ml_joinest_enabled=true; SET query_no=0; SET join_est_no=0; SET ml_joinest_fname='tmp_56.txt';"
                cur.execute(f"{setup} EXPLAIN {query}")
                lb_plan = cur.fetchall()

        new_ests_ub = ests[:i] + [ubs[i]] + ests[i+1:]
        with open("/mydata/stats_db/tmp_56.txt", "w") as f:
            for est in new_ests_lb:
                f.write(str(est) + "\n")

        with psycopg2.connect("dbname=stats user=yuxuan18") as conn:
            with conn.cursor() as cur:
                setup = "SET ml_joinest_enabled=true; SET query_no=0; SET join_est_no=0; SET ml_joinest_fname='tmp_56.txt';"
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

import time

sample_size = 80
u, p, t, b, v, u_sample, p_sample, sample_rate_u, sample_rate_p = prepare_date(sample_size)
start = time.time()
lbs, ubs, ests = estimate(u_sample, p_sample, p, t, b, v, sample_rate_u, sample_rate_p)
print("Time:", time.time() - start)
print(lbs, ubs, ests)
reward = explain(lbs, ubs, ests)
print(reward)
