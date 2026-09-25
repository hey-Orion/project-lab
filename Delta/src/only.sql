create table customers (
    customer_id integer primary key,
    name text,
    country text,
    signup_date date
);

create table orders (
    order_id integer primary key,
    customer_id integer,
    order_date date,
    amount float,
    status text
);

create table order_items (
    order_id integer,
    product_id integer,
    quantity integer
);

create table products (
    product_id integer primary key,
    name text,
    category text,
    price float
);



select c.name, o.order_date, o.amount
from customers c 
join orders o on c.customer_id = o.customer_id
where o.status = 'completed' and o.amount > 200;

select c.country sum(amount) as total_revenue
from customers c 
join orders o on c.customer_id = o.customer_id
where  o.status = 'completed'
having count(o.order_id) > 10;

select p.category sum(oi.quantity) as total_units
from order_items oi 
join products p on oi.product_id = p.product_id
group by p.category
order by total_units desc;

select
    customer_id, order_id, amount,
    lag(amount) over (partition by customer_id order by order_date) as 
    prev_amount
from orders;

select
    customer_id, order_date, amount,
    sum(amount) over (partition by customer_id order by order_date) as 
    running_total
from orders;

with ranked as (
    select 
        customer_id, order_id, amount,
        rank() over (partition by customer_id order by amount desc) as rank
    from orders 
)
select customer_id, order_id, amount
from ranked
where rnk = 1;

with customer_totals as (
    select customer_id, sum(amount) as total_amount
    from orders 
    group by customer_id
)
select customer_id, total_amount
from customer_totals
where total_amount > (select avg(total_amount) from customer_totals);

with customer_totals as (
    select customer_id, sum(amount) as total_amount
    from orders 
    group by customer_id
),
ranked as (
    select 
        customer_id, total_amount,
        percent_rank() over (order by total_amount desc) as pct_rank 
    from customer_totals
)
select customer_id, total_amount
from ranked
where pct_rank <= 0.10;