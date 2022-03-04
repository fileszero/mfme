import mylib
import mfme_client


me_config = mylib.get_config("mfme_account_requery.json")

mfme = mfme_client.mfme_client(me_config["mfme"])

mfme.requery_account(me_config["mfme"]["accounts"])