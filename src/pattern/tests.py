from elasticsearch import Elasticsearch, helpers

es = Elasticsearch()
body = {
    "size": 200,
    "query": {
        "match_all": {

        }
    },
    "sort": [
        {
            "year": {
                "order": "desc"
            }
        }
    ]

}
res = es.search(index='articles', body=body)
for data in res['hits']['hits']:
    print(data['_source']['title'])
    print(data['_source']['year'])

# action = [
#     {
#         "_index": "articles",
#         "_type": "doc",
#         "_source": {
#             "id": "53e99e61b7602d97027281bf",
#             "title": "Anti-caism of survivin siRNA plasmid mU6/survivin",
#             "authors": ["LI Li-ping", "ZHANG Zhi-zhen", ],
#             "year": 1234,
#             "keywords": ["siRNA plasmid", "survivin", "breast cancer cells", "mitotic cell death"],
#             "abstract": "Objective:To study inhibitory effects of survivin siRNA plasmid(mU6/survivin)constructed and reported on proliferation of breast cancer cells MCF-7 and its mechanism.Methods:Effect of plasmid mU6/survivin on the cell proliferation was analysed by MTT assay,on the cell cycle by flow cytometry,on the cell morphology by Hoechst staining,and then the activity of caspase-3 change was determined by its substrate Ac-DEVD-pNA,and some related proteins expression were detected by Western blot.Results:After transfected with plasmid mU6/survivin,the proliferation of MCF-7 cells were inhibited significantly,cell cycle arrested in G1 phase during 36 h,cells turned to be multinuclear and macronucleus.Protein caspase-3 expressed increasely and was activated,proteins I \u03baB\u03b1 \u3001Cyt C and p21waf1 expressed increasely,however,no changes were found in expression of protein NF-\u03baB(p65).Conclusion:RNA interference of survivin on MCF-7 cells played a crucial role in cell proliferation and cell cycle progression,and its mechanisms might be related to the caspase cascade,mitochondria apoptosis pathway and cell cycle regulation process,and mitotic cell death might be the main cause of the cell death."
#         }
#
#     },
#     {
#         "_index": "articles",
#         "_type": "doc",
#         "_source": {
#             "id": "53e99e61b7602d97027281bf",
#             "title": "Anti-caism siRNA plasmid mU6/survivin",
#             "authors": ["LI Li-ping", "ZHANG Zhi-zhen", ],
#             "year": 1278,
#             "keywords": ["siRNA plasmid", "survivin", "breast cancer cells", "mitotic cell death"],
#             "abstract": "Objective:To study inhibitory effects of survivin siRNA plasmid(mU6/survivin)constructed and reported on proliferation of breast cancer cells MCF-7 and its mechanism.Methods:Effect of plasmid mU6/survivin on the cell proliferation was analysed by MTT assay,on the cell cycle by flow cytometry,on the cell morphology by Hoechst staining,and then the activity of caspase-3 change was determined by its substrate Ac-DEVD-pNA,and some related proteins expression were detected by Western blot.Results:After transfected with plasmid mU6/survivin,the proliferation of MCF-7 cells were inhibited significantly,cell cycle arrested in G1 phase during 36 h,cells turned to be multinuclear and macronucleus.Protein caspase-3 expressed increasely and was activated,proteins I \u03baB\u03b1 \u3001Cyt C and p21waf1 expressed increasely,however,no changes were found in expression of protein NF-\u03baB(p65).Conclusion:RNA interference of survivin on MCF-7 cells played a crucial role in cell proliferation and cell cycle progression,and its mechanisms might be related to the caspase cascade,mitochondria apoptosis pathway and cell cycle regulation process,and mitotic cell death might be the main cause of the cell death."
#         }
#
#     },
#     {
#         "_index": "articles",
#         "_type": "doc",
#         "_source": {
#             "id": "53e99e61b7602d97027281bf",
#             "title": "Anti-caism siRN/survivin",
#             "authors": ["LI Li-ping", "ZHANG Zhi-zhen", ],
#             "year": 1878,
#             "keywords": ["siRNA plasmid", "survivin", "breast cancer cells", "mitotic cell death"],
#             "abstract": "Objective:To study inhibitory effects of survivin siRNA plasmid(mU6/survivin)constructed and reported on proliferation of breast cancer cells MCF-7 and its mechanism.Methods:Effect of plasmid mU6/survivin on the cell proliferation was analysed by MTT assay,on the cell cycle by flow cytometry,on the cell morphology by Hoechst staining,and then the activity of caspase-3 change was determined by its substrate Ac-DEVD-pNA,and some related proteins expression were detected by Western blot.Results:After transfected with plasmid mU6/survivin,the proliferation of MCF-7 cells were inhibited significantly,cell cycle arrested in G1 phase during 36 h,cells turned to be multinuclear and macronucleus.Protein caspase-3 expressed increasely and was activated,proteins I \u03baB\u03b1 \u3001Cyt C and p21waf1 expressed increasely,however,no changes were found in expression of protein NF-\u03baB(p65).Conclusion:RNA interference of survivin on MCF-7 cells played a crucial role in cell proliferation and cell cycle progression,and its mechanisms might be related to the caspase cascade,mitochondria apoptosis pathway and cell cycle regulation process,and mitotic cell death might be the main cause of the cell death."
#         }
#
#     }
# ]
# helpers.bulk(es, action, request_timeout=1000)
