import sys
import json
import psycopg2
import psycopg2.extras
import pdb

db_connection = None
cursor = None
action = None

sql_queries = {
    "check_whitelist_exists": """SELECT "domain", app_ids FROM public.custom_domain_whitelist where domain=%s;""",
    "insert_new_whitelist_row": """INSERT INTO public.custom_domain_whitelist (domain, app_ids) VALUES (%s, %s);""",
    "update_whitelist_row": """UPDATE public.custom_domain_whitelist SET app_ids = %s WHERE domain = %s;""",
    "update_short_url_domain": """UPDATE app SET short_url_domain = %s WHERE id = %s;"""
}

def read_input():
    # Example: ./add-custom-domain-whitelist <linkdomain> <appid> <boolean - update short_url_domain>
    if len(sys.argv) != 4:
        abort("Correct Usage: ./add-custom-domain-whitelist link.joon.com 1234567890 true");
    else:
        print "parameters: %s %s %s" % (sys.argv[1], sys.argv[2], sys.argv[3])
        return sys.argv[1], sys.argv[2], sys.argv[3]

def connect_to_db(connection_string):
    try:
        global db_connection, cursor
        db_connection = psycopg2.connect(connection_string)
        cursor = db_connection.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        print "Connected to Database"
    except Exception as e:
        abort("Couldnt connect to Database", e)

def add_whitelist(custom_domain, app_id):
    try:
        cursor.execute(sql_queries["check_whitelist_exists"], [custom_domain])
        print "Running query:", sql_queries["check_whitelist_exists"] % custom_domain
        row = cursor.fetchone()        
        
        if row == None:
            print "Row Empty. Inserting new row..."
            appids = [long(app_id)]
            print appids
            cursor.execute(sql_queries["insert_new_whitelist_row"], [custom_domain, appids])
            db_connection.commit()
            print "Finished creating new row"
        else:
            if custom_domain == row[0] and long(app_id) in row[1]:
                abort("The entry already exists.")
            else:
                print "Row exists. Adding record." 
                appids = row[1]
                appids.append(long(app_id))
                cursor.execute(sql_queries["update_whitelist_row"], [appids, custom_domain])
                db_connection.commit()
                print "Finished adding to existing row"
    except Exception as e:
        abort("Failed in [add_whitelist]", e)

def add_short_url_domain(custom_domain, app_id):
    try:    
        cursor.execute(sql_queries["update_short_url_domain"], [custom_domain, app_id])
        db_connection.commit()
        print "Finished updating short_url_domain"
    except Exception as e:
        abort("Failed in [add_short_url_domain]", e)


def abort(message, error=None):
    print (message, error)
    print ("Aborting...")
    if cursor is not None:
        cursor.close()
    if db_connection is not None:
        db_connection.close()
    sys.exit()

def run():
    custom_domain, appid, addshorturldomain = read_input()
    print custom_domain
    print appid
    print addshorturldomain

    global action
    with open("/var/app/config.json") as data_file:
        config = json.load(data_file)
        # should eventually add this to config.json
        connectionString = config["postgres_analytics"].replace("/analytics", "/link")
        connect_to_db(connectionString)
        add_whitelist(custom_domain, appid)

        if addshorturldomain == 'true':
            connect_to_db(config["postgres_core"])
            add_short_url_domain(custom_domain, appid)

        print "We're done here!"
run()