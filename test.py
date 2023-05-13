import firestore

# coll_ref = firestore.firestore_client.collection("classifications")
# create_time, doc_ref = coll_ref.add(
#     {
#         "classification": 2,
        
#     }
# )

doc_ref = firestore.firestore_client.collection("classifications").document("1")
doc_ref.set(
    {
        "classification": 0,
    }
)