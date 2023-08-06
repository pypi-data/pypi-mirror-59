sparktool
========
built to simplified the process of creating sparksession(hccn).
* can get saved query from hue
* batch execute multiple sqls which are from same sql scripts
* can parse impala/hive view automatically
* can parse kudu table automatically

what's new
========
* get saved query from hue

install
=======

Python 2/3 

* `pip install --user --upgrade sparktool`
* `pip2 install --user --upgrade sparktool`

functions
=======

switch_keytab (first run)
--------
import sparktool as st
st.switch_keytab('admin@EXAMPLE.COM', keytabpath)
```

switch_keytab (first run)
--------
import sparktool as st
st.switch_huetab('admin@EXAMPLE.COM', keytabpath)
```

batch_excutesql
--------
[in]

```python
# encoding=utf-8
import sparktool as st

ss = st.SparkCreator()
sql = '''
select 1;
select
    cc.skp_client
from
    owner_ogg.ft_ccase_2_ccase_ad cc
    join owner_ogg.clt_ccase_2_ccase_relation re
      on cc.skp_ccase_2_ccase_relation = re.skp_ccase_2_ccase_relation
     and re.code_ccase_relation = 'FIRST_POS' 
limit 1
;
'''
ss.batch_excutesql(sql)
```

[out]

```python
Tranform Table:
+--------------------------------------+--------------------------------------+--------------+
|             Origin Table             |            Temporary View            | If Transform |
+--------------------------------------+--------------------------------------+--------------+
|    OWNER_OGG.FT_CCASE_2_CCASE_AD     |    owner_ogg_ft_ccase_2_ccase_ad     |     New      |
| OWNER_OGG.CLT_CCASE_2_CCASE_RELATION | owner_ogg_clt_ccase_2_ccase_relation |     New      |
+--------------------------------------+--------------------------------------+--------------+
Excute Progress: 2/2
DataFrame[skp_client: decimal(38,0)]
```


[in]

```python
# encoding=utf-8
import sparktool as st

ss = st.SparkCreator()
sql = '''
select * from winnie_wangtjww.hcp_crm_offer limit 1;
drop table if exists ttttttttt;
select 1 as tt;
select * from ap_crm.ft_sas_segment_client limit 1;
select * from owner_ogg.ft_mobile_app_user_ad limit 1;
'''
b,c,d,e,f = ss.batch_excutesql(sql, ifview=True, ifbatchre=True)
```

[out]

```python
Tranform Table:
+-----------------------------------------+-----------------------------------------------+--------------+
|               Origin Table              |                   Kudu Table                  | If Transform |
+-----------------------------------------+-----------------------------------------------+--------------+
|        hadoop_dl.dct_sas_campaign       |        impala::AP_ITBD.dct_sas_campaign       |    Added     |
|     hadoop_dl.dct_sas_communication     |     impala::ap_itbd.dct_sas_communication     |    Added     |
|        hadoop_dl.dct_sas_segment        |        impala::ap_itbd.dct_sas_segment        |    Added     |
|   owner_ogg.dct_capp_message_template   |  impala::OWNER_OGG.DCT_CAPP_MESSAGE_TEMPLATE  |    Added     |
|        owner_ogg.dct_sms_template       |       impala::OWNER_OGG.DCT_SMS_TEMPLATE      |    Added     |
|     hadoop_dl.clt_sas_contact_status    |     impala::ap_itbd.clt_sas_contact_status    |    Added     |
| hadoop_dl.ft_sas_camp_segment_client_at | impala::AP_ITBD.ft_sas_camp_segment_client_at |    Added     |
|  hadoop_dl.ft_sas_segment_treatment_tt  |  impala::AP_ITBD.ft_sas_segment_treatment_tt  |    Added     |
|      winnie_wangtjww.hcp_crm_offer      |                      None                     |      No      |
|      owner_ogg.dct_wechat_template      |     impala::OWNER_OGG.DCT_WECHAT_TEMPLATE     |    Added     |
|          hadoop_dl.dct_sas_cell         |          impala::AP_ITBD.dct_sas_cell         |    Added     |
|     owner_ogg.ft_mobile_app_user_ad     |    impala::OWNER_OGG.FT_MOBILE_APP_USER_AD    |    Added     |
+-----------------------------------------+-----------------------------------------------+--------------+
Excute Progress: 5/5
```

batch_excutesql
--------
[in]
```python
# encoding=utf-8
from sparktool import HueCreator
aa  = HueCreator()
aa.query_printlist()
```
[out]
```python
+--------+-------------------------+----------------------------+-------------------+
|   id   |           name          |        description         |   last_modified   |
+--------+-------------------------+----------------------------+-------------------+
| 691124 |     aaaaaaaaaaaaaaa     |                            | 2020-01-17T17:41Z |
| 686849 |           hcp           |                            | 2020-01-17T10:32Z |
| 675390 |           aaaa          |                            | 2020-01-16T11:05Z |
| 681235 |          ttttt          |                            | 2020-01-15T09:41Z |
| 676699 |           aaaa          |                            | 2020-01-14T09:53Z | |
+--------+-------------------------+----------------------------+-------------------+
```

[in]
```python
# encoding=utf-8
aa.query_getscript('hcp')
```
