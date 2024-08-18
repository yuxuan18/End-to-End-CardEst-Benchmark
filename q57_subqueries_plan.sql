SELECT COUNT(*) 
FROM postLinks as pl, posts as p 
WHERE p.Id = pl.RelatedPostId AND p.CommentCount>=0 AND p.CommentCount<=13;

SELECT COUNT(*) 
FROM postHistory as ph, posts as p, users as u 
WHERE u.Id = p.OwnerUserId AND u.Id = ph.UserId AND ph.PostHistoryTypeId=5 AND ph.CreationDate<='2014-08-13 09:20:10'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13;

SELECT COUNT(*) 
FROM votes as v, posts as p, users as u 
WHERE u.Id = p.OwnerUserId AND u.Id = v.UserId AND v.CreationDate>='2010-07-19 00:00:00'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13;

SELECT COUNT(*) 
FROM badges as b, posts as p, users as u 
WHERE u.Id = p.OwnerUserId AND u.Id = b.UserId AND b.Date<='2014-09-09 10:24:35'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13;

SELECT COUNT(*) 
FROM users as u, posts as p 
WHERE u.Id = p.OwnerUserId AND u.Views>=0 AND u.DownVotes>=0 AND u.CreationDate>='2010-08-04 16:59:53'::timestamp AND u.CreationDate<='2014-07-22 15:15:22'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13;

SELECT COUNT(*) 
FROM votes as v, postHistory as ph, users as u 
WHERE u.Id = v.UserId AND u.Id = ph.UserId AND v.CreationDate>='2010-07-19 00:00:00'::timestamp AND ph.PostHistoryTypeId=5 AND ph.CreationDate<='2014-08-13 09:20:10'::timestamp;

SELECT COUNT(*) 
FROM badges as b, postHistory as ph, users as u 
WHERE u.Id = b.UserId AND u.Id = ph.UserId AND b.Date<='2014-09-09 10:24:35'::timestamp AND ph.PostHistoryTypeId=5 AND ph.CreationDate<='2014-08-13 09:20:10'::timestamp;

SELECT COUNT(*) 
FROM users as u, postHistory as ph 
WHERE u.Id = ph.UserId AND u.Views>=0 AND u.DownVotes>=0 AND u.CreationDate>='2010-08-04 16:59:53'::timestamp AND u.CreationDate<='2014-07-22 15:15:22'::timestamp AND ph.PostHistoryTypeId=5 AND ph.CreationDate<='2014-08-13 09:20:10'::timestamp;

SELECT COUNT(*) 
FROM badges as b, votes as v, users as u 
WHERE u.Id = b.UserId AND u.Id = v.UserId AND b.Date<='2014-09-09 10:24:35'::timestamp AND v.CreationDate>='2010-07-19 00:00:00'::timestamp;

SELECT COUNT(*) 
FROM users as u, votes as v 
WHERE u.Id = v.UserId AND u.Views>=0 AND u.DownVotes>=0 AND u.CreationDate>='2010-08-04 16:59:53'::timestamp AND u.CreationDate<='2014-07-22 15:15:22'::timestamp AND v.CreationDate>='2010-07-19 00:00:00'::timestamp;

SELECT COUNT(*) 
FROM users as u, badges as b 
WHERE u.Id = b.UserId AND u.Views>=0 AND u.DownVotes>=0 AND u.CreationDate>='2010-08-04 16:59:53'::timestamp AND u.CreationDate<='2014-07-22 15:15:22'::timestamp AND b.Date<='2014-09-09 10:24:35'::timestamp;

SELECT COUNT(*) 
FROM postHistory as ph, posts as p, postLinks as pl, users as u 
WHERE u.Id = p.OwnerUserId AND p.Id = pl.RelatedPostId AND u.Id = ph.UserId AND ph.PostHistoryTypeId=5 AND ph.CreationDate<='2014-08-13 09:20:10'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13;

SELECT COUNT(*) 
FROM votes as v, posts as p, postLinks as pl, users as u 
WHERE u.Id = p.OwnerUserId AND p.Id = pl.RelatedPostId AND u.Id = v.UserId AND v.CreationDate>='2010-07-19 00:00:00'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13;

SELECT COUNT(*) 
FROM badges as b, posts as p, postLinks as pl, users as u 
WHERE u.Id = p.OwnerUserId AND p.Id = pl.RelatedPostId AND u.Id = b.UserId AND b.Date<='2014-09-09 10:24:35'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13;

SELECT COUNT(*) 
FROM users as u, posts as p, postLinks as pl 
WHERE u.Id = p.OwnerUserId AND p.Id = pl.RelatedPostId AND u.Views>=0 AND u.DownVotes>=0 AND u.CreationDate>='2010-08-04 16:59:53'::timestamp AND u.CreationDate<='2014-07-22 15:15:22'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13;

SELECT COUNT(*) 
FROM votes as v, posts as p, postHistory as ph, users as u 
WHERE u.Id = p.OwnerUserId AND u.Id = v.UserId AND u.Id = ph.UserId AND v.CreationDate>='2010-07-19 00:00:00'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13 AND ph.PostHistoryTypeId=5 AND ph.CreationDate<='2014-08-13 09:20:10'::timestamp;

SELECT COUNT(*) 
FROM badges as b, posts as p, postHistory as ph, users as u 
WHERE u.Id = p.OwnerUserId AND u.Id = b.UserId AND u.Id = ph.UserId AND b.Date<='2014-09-09 10:24:35'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13 AND ph.PostHistoryTypeId=5 AND ph.CreationDate<='2014-08-13 09:20:10'::timestamp;

SELECT COUNT(*) 
FROM users as u, posts as p, postHistory as ph 
WHERE u.Id = p.OwnerUserId AND u.Id = ph.UserId AND u.Views>=0 AND u.DownVotes>=0 AND u.CreationDate>='2010-08-04 16:59:53'::timestamp AND u.CreationDate<='2014-07-22 15:15:22'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13 AND ph.PostHistoryTypeId=5 AND ph.CreationDate<='2014-08-13 09:20:10'::timestamp;

SELECT COUNT(*) 
FROM badges as b, posts as p, votes as v, users as u 
WHERE u.Id = p.OwnerUserId AND u.Id = b.UserId AND u.Id = v.UserId AND b.Date<='2014-09-09 10:24:35'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13 AND v.CreationDate>='2010-07-19 00:00:00'::timestamp;

SELECT COUNT(*) 
FROM users as u, posts as p, votes as v 
WHERE u.Id = p.OwnerUserId AND u.Id = v.UserId AND u.Views>=0 AND u.DownVotes>=0 AND u.CreationDate>='2010-08-04 16:59:53'::timestamp AND u.CreationDate<='2014-07-22 15:15:22'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13 AND v.CreationDate>='2010-07-19 00:00:00'::timestamp;

SELECT COUNT(*) 
FROM users as u, posts as p, badges as b 
WHERE u.Id = p.OwnerUserId AND u.Id = b.UserId AND u.Views>=0 AND u.DownVotes>=0 AND u.CreationDate>='2010-08-04 16:59:53'::timestamp AND u.CreationDate<='2014-07-22 15:15:22'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13 AND b.Date<='2014-09-09 10:24:35'::timestamp;

SELECT COUNT(*) 
FROM badges as b, postHistory as ph, votes as v, users as u 
WHERE u.Id = b.UserId AND u.Id = v.UserId AND u.Id = ph.UserId AND b.Date<='2014-09-09 10:24:35'::timestamp AND ph.PostHistoryTypeId=5 AND ph.CreationDate<='2014-08-13 09:20:10'::timestamp AND v.CreationDate>='2010-07-19 00:00:00'::timestamp;

SELECT COUNT(*) 
FROM users as u, postHistory as ph, votes as v 
WHERE u.Id = v.UserId AND u.Id = ph.UserId AND u.Views>=0 AND u.DownVotes>=0 AND u.CreationDate>='2010-08-04 16:59:53'::timestamp AND u.CreationDate<='2014-07-22 15:15:22'::timestamp AND ph.PostHistoryTypeId=5 AND ph.CreationDate<='2014-08-13 09:20:10'::timestamp AND v.CreationDate>='2010-07-19 00:00:00'::timestamp;

SELECT COUNT(*) 
FROM users as u, postHistory as ph, badges as b 
WHERE u.Id = b.UserId AND u.Id = ph.UserId AND u.Views>=0 AND u.DownVotes>=0 AND u.CreationDate>='2010-08-04 16:59:53'::timestamp AND u.CreationDate<='2014-07-22 15:15:22'::timestamp AND ph.PostHistoryTypeId=5 AND ph.CreationDate<='2014-08-13 09:20:10'::timestamp AND b.Date<='2014-09-09 10:24:35'::timestamp;

SELECT COUNT(*) 
FROM users as u, votes as v, badges as b 
WHERE u.Id = b.UserId AND u.Id = v.UserId AND u.Views>=0 AND u.DownVotes>=0 AND u.CreationDate>='2010-08-04 16:59:53'::timestamp AND u.CreationDate<='2014-07-22 15:15:22'::timestamp AND v.CreationDate>='2010-07-19 00:00:00'::timestamp AND b.Date<='2014-09-09 10:24:35'::timestamp;

SELECT COUNT(*) 
FROM votes as v, posts as p, postLinks as pl, postHistory as ph, users as u 
WHERE u.Id = p.OwnerUserId AND p.Id = pl.RelatedPostId AND u.Id = v.UserId AND u.Id = ph.UserId AND v.CreationDate>='2010-07-19 00:00:00'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13 AND ph.PostHistoryTypeId=5 AND ph.CreationDate<='2014-08-13 09:20:10'::timestamp;

SELECT COUNT(*) 
FROM badges as b, posts as p, postLinks as pl, postHistory as ph, users as u 
WHERE u.Id = p.OwnerUserId AND p.Id = pl.RelatedPostId AND u.Id = b.UserId AND u.Id = ph.UserId AND b.Date<='2014-09-09 10:24:35'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13 AND ph.PostHistoryTypeId=5 AND ph.CreationDate<='2014-08-13 09:20:10'::timestamp;

SELECT COUNT(*) 
FROM users as u, posts as p, postLinks as pl, postHistory as ph 
WHERE u.Id = p.OwnerUserId AND p.Id = pl.RelatedPostId AND u.Id = ph.UserId AND u.Views>=0 AND u.DownVotes>=0 AND u.CreationDate>='2010-08-04 16:59:53'::timestamp AND u.CreationDate<='2014-07-22 15:15:22'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13 AND ph.PostHistoryTypeId=5 AND ph.CreationDate<='2014-08-13 09:20:10'::timestamp;

SELECT COUNT(*) 
FROM badges as b, posts as p, postLinks as pl, votes as v, users as u 
WHERE u.Id = p.OwnerUserId AND p.Id = pl.RelatedPostId AND u.Id = b.UserId AND u.Id = v.UserId AND b.Date<='2014-09-09 10:24:35'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13 AND v.CreationDate>='2010-07-19 00:00:00'::timestamp;

SELECT COUNT(*) 
FROM users as u, posts as p, postLinks as pl, votes as v 
WHERE u.Id = p.OwnerUserId AND p.Id = pl.RelatedPostId AND u.Id = v.UserId AND u.Views>=0 AND u.DownVotes>=0 AND u.CreationDate>='2010-08-04 16:59:53'::timestamp AND u.CreationDate<='2014-07-22 15:15:22'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13 AND v.CreationDate>='2010-07-19 00:00:00'::timestamp;

SELECT COUNT(*) 
FROM users as u, posts as p, postLinks as pl, badges as b 
WHERE p.Id = pl.RelatedPostId AND u.Id = p.OwnerUserId AND u.Id = b.UserId AND u.Views>=0 AND u.DownVotes>=0 AND u.CreationDate>='2010-08-04 16:59:53'::timestamp AND u.CreationDate<='2014-07-22 15:15:22'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13 AND b.Date<='2014-09-09 10:24:35'::timestamp;

SELECT COUNT(*) 
FROM badges as b, posts as p, postHistory as ph, votes as v, users as u 
WHERE u.Id = p.OwnerUserId AND u.Id = b.UserId AND u.Id = v.UserId AND u.Id = ph.UserId AND b.Date<='2014-09-09 10:24:35'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13 AND ph.PostHistoryTypeId=5 AND ph.CreationDate<='2014-08-13 09:20:10'::timestamp AND v.CreationDate>='2010-07-19 00:00:00'::timestamp;

SELECT COUNT(*) 
FROM users as u, posts as p, postHistory as ph, votes as v 
WHERE u.Id = p.OwnerUserId AND u.Id = v.UserId AND u.Id = ph.UserId AND u.Views>=0 AND u.DownVotes>=0 AND u.CreationDate>='2010-08-04 16:59:53'::timestamp AND u.CreationDate<='2014-07-22 15:15:22'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13 AND ph.PostHistoryTypeId=5 AND ph.CreationDate<='2014-08-13 09:20:10'::timestamp AND v.CreationDate>='2010-07-19 00:00:00'::timestamp;

SELECT COUNT(*) 
FROM users as u, posts as p, postHistory as ph, badges as b 
WHERE u.Id = p.OwnerUserId AND u.Id = b.UserId AND u.Id = ph.UserId AND u.Views>=0 AND u.DownVotes>=0 AND u.CreationDate>='2010-08-04 16:59:53'::timestamp AND u.CreationDate<='2014-07-22 15:15:22'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13 AND ph.PostHistoryTypeId=5 AND ph.CreationDate<='2014-08-13 09:20:10'::timestamp AND b.Date<='2014-09-09 10:24:35'::timestamp;

SELECT COUNT(*) 
FROM users as u, posts as p, votes as v, badges as b 
WHERE u.Id = p.OwnerUserId AND u.Id = b.UserId AND u.Id = v.UserId AND u.Views>=0 AND u.DownVotes>=0 AND u.CreationDate>='2010-08-04 16:59:53'::timestamp AND u.CreationDate<='2014-07-22 15:15:22'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13 AND v.CreationDate>='2010-07-19 00:00:00'::timestamp AND b.Date<='2014-09-09 10:24:35'::timestamp;

SELECT COUNT(*) 
FROM users as u, postHistory as ph, votes as v, badges as b 
WHERE u.Id = b.UserId AND u.Id = v.UserId AND u.Id = ph.UserId AND u.Views>=0 AND u.DownVotes>=0 AND u.CreationDate>='2010-08-04 16:59:53'::timestamp AND u.CreationDate<='2014-07-22 15:15:22'::timestamp AND ph.PostHistoryTypeId=5 AND ph.CreationDate<='2014-08-13 09:20:10'::timestamp AND v.CreationDate>='2010-07-19 00:00:00'::timestamp AND b.Date<='2014-09-09 10:24:35'::timestamp;

SELECT COUNT(*) 
FROM badges as b, posts as p, postLinks as pl, postHistory as ph, votes as v, users as u 
WHERE u.Id = p.OwnerUserId AND u.Id = b.UserId AND u.Id = ph.UserId AND p.Id = pl.RelatedPostId AND u.Id = v.UserId AND b.Date<='2014-09-09 10:24:35'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13 AND ph.PostHistoryTypeId=5 AND ph.CreationDate<='2014-08-13 09:20:10'::timestamp AND v.CreationDate>='2010-07-19 00:00:00'::timestamp;

SELECT COUNT(*) 
FROM users as u, posts as p, postLinks as pl, postHistory as ph, votes as v 
WHERE u.Id = p.OwnerUserId AND p.Id = pl.RelatedPostId AND u.Id = v.UserId AND u.Id = ph.UserId AND u.Views>=0 AND u.DownVotes>=0 AND u.CreationDate>='2010-08-04 16:59:53'::timestamp AND u.CreationDate<='2014-07-22 15:15:22'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13 AND ph.PostHistoryTypeId=5 AND ph.CreationDate<='2014-08-13 09:20:10'::timestamp AND v.CreationDate>='2010-07-19 00:00:00'::timestamp;

SELECT COUNT(*) 
FROM users as u, posts as p, postLinks as pl, postHistory as ph, badges as b 
WHERE p.Id = pl.RelatedPostId AND u.Id = p.OwnerUserId AND u.Id = b.UserId AND u.Id = ph.UserId AND u.Views>=0 AND u.DownVotes>=0 AND u.CreationDate>='2010-08-04 16:59:53'::timestamp AND u.CreationDate<='2014-07-22 15:15:22'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13 AND ph.PostHistoryTypeId=5 AND ph.CreationDate<='2014-08-13 09:20:10'::timestamp AND b.Date<='2014-09-09 10:24:35'::timestamp;

SELECT COUNT(*) 
FROM users as u, posts as p, postLinks as pl, votes as v, badges as b 
WHERE p.Id = pl.RelatedPostId AND u.Id = p.OwnerUserId AND u.Id = b.UserId AND u.Id = v.UserId AND u.Views>=0 AND u.DownVotes>=0 AND u.CreationDate>='2010-08-04 16:59:53'::timestamp AND u.CreationDate<='2014-07-22 15:15:22'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13 AND v.CreationDate>='2010-07-19 00:00:00'::timestamp AND b.Date<='2014-09-09 10:24:35'::timestamp;

SELECT COUNT(*) 
FROM users as u, posts as p, postHistory as ph, votes as v, badges as b 
WHERE u.Id = p.OwnerUserId AND u.Id = b.UserId AND u.Id = v.UserId AND u.Id = ph.UserId AND u.Views>=0 AND u.DownVotes>=0 AND u.CreationDate>='2010-08-04 16:59:53'::timestamp AND u.CreationDate<='2014-07-22 15:15:22'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13 AND ph.PostHistoryTypeId=5 AND ph.CreationDate<='2014-08-13 09:20:10'::timestamp AND v.CreationDate>='2010-07-19 00:00:00'::timestamp AND b.Date<='2014-09-09 10:24:35'::timestamp;

SELECT COUNT(*) 
FROM users as u, posts as p, postLinks as pl, postHistory as ph, votes as v, badges as b 
WHERE u.Id = p.OwnerUserId AND u.Id = b.UserId AND u.Id = ph.UserId AND p.Id = pl.RelatedPostId AND u.Id = v.UserId AND u.Views>=0 AND u.DownVotes>=0 AND u.CreationDate>='2010-08-04 16:59:53'::timestamp AND u.CreationDate<='2014-07-22 15:15:22'::timestamp AND p.CommentCount>=0 AND p.CommentCount<=13 AND ph.PostHistoryTypeId=5 AND ph.CreationDate<='2014-08-13 09:20:10'::timestamp AND v.CreationDate>='2010-07-19 00:00:00'::timestamp AND b.Date<='2014-09-09 10:24:35'::timestamp;
