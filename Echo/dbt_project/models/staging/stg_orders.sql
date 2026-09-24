select
    order_id,
    customer_id,
    order_date,
    amount,
    lower(trim(status)) as status 
from {{ source('raw', 'orders') }}
where amount is NOT NULL
