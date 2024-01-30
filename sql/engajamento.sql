select id,
owner_username,
url, 
sum(likes_count) + sum(comments_count) as engagement
from instagram_posts_mage ipm 
where owner_username  = 'xxxx'
group by id, owner_username, url, comments_count