select
    customer_id,
    sum(amount) as total_revenue,
    count(order_id) as total_orders
from {{ ref('stg_orders') }} # this block
where status = 'completed'
group by customer_id
