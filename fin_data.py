import requests
import json

def lambda_handler(req, context):

  query = """
  {
    repays{
        id
        timestamp
        account{
        id
        }
        market {
        id
        }
        asset{
        id
        symbol
        }
        amount
        amountUSD
    }
        borrows {
            id
        timestamp
        account{
            id
        }
        market {
            id
        }
        asset{
            id
            symbol
        }
        amount
        amountUSD
    }
        withdraws {
            id
        timestamp
        account{
            id
        }
        market {
            id
        }
        asset{
            id
            symbol
        }
        amount
        amountUSD
    }
        deposits {
            id
        timestamp
        account{
            id
        }
        market {
            id
        }
        asset{
            id
            symbol
        }
        amount
        amountUSD
    }
        liquidates {
            id
        timestamp
        liquidator{
            id
        }
        liquidatee{
            id
        }
        market {
            id
        }
        asset{
            id
            symbol
        }
        amount
        amountUSD
    }
  }
  """
  url = 'https://api.thegraph.com/subgraphs/name/messari/compound-ethereum'
  r = requests.post(url, json={'query': query})

  # You can parse this data into any form you'd like
  json_data = json.loads(r.text)

  # print(json_data)
  since_id = None
  dataext = None #json_data["data"].items() #json.loads(result.text)
  eventsData = []

  for k in json_data["data"].keys():
  
    dataext = json_data["data"][k]
    # Reformat response into nice, flat tables
    for t in dataext:
        # Remember the first id we encounter, which is the most recent
        if (since_id == None) :
            since_id = t["id"]

        # Add all eventsData
        eventsData.append({
            "event_type": k,
            "id": t["id"],
            "timestamp": t["timestamp"], 
            "event_payload": t
        })

  # Send JSON response back to Fivetran

  if(since_id==None):
      since_id = req.state.since_id
  ans = {
      # // Remember the most recent id, so our requests are incremental
      "state": {
          since_id: since_id
      },
      "schema" : {
          "eventsData" : {
              "primary_key" : ["id"]
          }
      },
      "insert": {
          "eventsData": eventsData
      },
      "hasMore" : False
  }
  return ans;
