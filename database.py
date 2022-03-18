import psycopg2


def database(user, repo, branch, sha, mess, comm):
    hostname = 'localhost'
    database_name = 'zadanie'
    username = 'postgres'
    passtod = 'baranek'
    port_id = 5050
    curs = None
    connect = None

    try:
        connect = psycopg2.connect(
            host=hostname,
            dbname=database_name,
            user=username,
            password=passtod,
            port=port_id)

        curs = connect.cursor()
        create_script = ''' CREATE TABLE IF NOT EXISTS all_commits(
                                    user_name   varchar(100),
                                    repository  varchar(100),
                                    branch      varchar(100),
                                    sha         varchar(100) PRIMARY KEY,
                                    message     varchar(500),
                                    committer   varchar(100)) '''
        create_user = ''' CREATE TABLE IF NOT EXISTS users(
                                    id          SERIAL,
                                    user_name   varchar(100) PRIMARY KEY)'''
        create_repo = ''' CREATE TABLE IF NOT EXISTS repositories(
                                    id          SERIAL,
                                    repository  varchar(100) PRIMARY KEY)'''
        create_branch = ''' CREATE TABLE IF NOT EXISTS branches(
                                    id          SERIAL,
                                    branch      varchar(100) PRIMARY KEY)'''

        curs.execute(create_script)
        curs.execute(create_user)
        curs.execute(create_repo)
        curs.execute(create_branch)
        connect.commit()

        insert_script = 'INSERT INTO all_commits (user_name, repository, branch, sha, message, committer) ' \
                        'VALUES (%s, %s, %s, %s, %s, %s) ' \
                        'ON CONFLICT (sha)  DO NOTHING' \

        insert_script_value = (user, repo, branch, sha, mess, comm)
        curs.execute(insert_script, insert_script_value)

        insert_user = 'INSERT INTO users(user_name) ' \
                      'VALUES (%s)' \
                      'ON CONFLICT (user_name) DO NOTHING'
        insert_user_values = (user,)
        curs.execute(insert_user, insert_user_values)

        insert_repo = 'INSERT INTO repositories(repository) ' \
                      'VALUES (%s)' \
                      'ON CONFLICT (repository) DO NOTHING'
        insert_repo_values = (repo,)
        curs.execute(insert_repo, insert_repo_values)

        insert_branch = 'INSERT INTO branches(branch) ' \
                        'VALUES (%s)' \
                        'ON CONFLICT (branch) DO NOTHING'
        insert_branch_values = (branch,)
        curs.execute(insert_branch, insert_branch_values)
        connect.commit()

    except Exception as err:
        print(err)
    finally:
        if curs is not None:
            curs.close()
        if connect is not None:
            connect.close()

