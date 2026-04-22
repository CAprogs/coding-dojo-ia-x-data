

select *
from read_parquet('{{ get_today_file("parquet") }}')
