from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from db_object import ms_request_type, tr_roles_permissions, tr_users
from db_connection import create_url


##############################
# table join
##############################

def read_user_request_type(connection_engine, username: str, request_method: str):
    """
    select
        u.username
        ,rt.request_type
    from
        main.tr_users u 
        left join 
        main.tr_roles_permissions rp 
        on
            u.roles_id = rp.roles_id
        left join
        main.ms_request_type rt 
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
            select(tr_users.username, ms_request_type.request_type)
            .join(tr_roles_permissions, tr_users.roles_id == tr_roles_permissions.roles_id, isouter = True)
            .join(ms_request_type, tr_roles_permissions.request_type_id == ms_request_type.id, isouter = True)
            .where(tr_roles_permissions.is_active == 1)
            .where(tr_users.username == username)
            .where(ms_request_type.request_type == request_method)
        )
        data = session.execute(stmt, execution_options={"prebuffer_rows": True}).first()
        return data


if __name__ == "__main__":
    url = create_url(ordinal = 1, database_product = "postgresql")
    engine = create_engine(url)
    data = read_user_request_type(engine, "admin", "POST")
    print(data.username, data.request_type)