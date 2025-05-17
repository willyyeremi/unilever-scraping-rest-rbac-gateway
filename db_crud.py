from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from db_object import request_type, roles_permissions, users
from db_connection import create_url


##############################
# table join
##############################

def read_user_request_type(connection_engine, username: str, request_method):
    """
    select
        u.username
        ,rt.request_type
    from
        public.users u 
        left join 
        public.roles_permissions rp 
        on
            u.roles_id = rp.roles_id
        left join
        request_type rt 
        on
            rp.request_type_id  = rt.id
    where
        rp.is_active = 1
        and
        u.username = <username>
        and
        rt.request_type = <request_method>
    """
    with Session(autocommit = False, autoflush = False, bind = connection_engine) as session:
        stmt = (
            select(users.username, request_type.request_type)
            .join(roles_permissions, users.roles_id == roles_permissions.roles_id, isouter = True)
            .join(request_type, roles_permissions.request_type_id == request_type.id, isouter = True)
            .where(roles_permissions.is_active == 1)
            .where(users.username == username)
            .where(request_type.request_type == request_method)
        )
        data = session.execute(stmt, execution_options={"prebuffer_rows": True}).first()
        return data


if __name__ == "__main__":
    url = create_url(ordinal = 1, database_product = "postgresql")
    engine = create_engine(url)
    data = read_user_request_type(engine, "admin", "POST")
    print(data.username, data.request_type)