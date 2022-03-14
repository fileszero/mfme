import sys
import mylib
import mfme_client


config_file="mfme_account_requery.json"
if sys.argv[1:2]:
    config_file=sys.argv[1]


me_config = mylib.get_config(config_file)

mfme = mfme_client.mfme_client(me_config["mfme"])

mfme.requery_account(me_config["mfme"]["accounts"])