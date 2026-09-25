select
    order_id,
    customer_id,
    order_date,
    amount,
    LOWER(TRIM(status)) AS status # this block
from {{ source('raw_data', 'orders') }}
where amount is not null
