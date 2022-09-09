import requests
import json

def lambda_handler(req, context):

  query = """{
    financialsDailySnapshots{
      id
      totalValueLockedUSD
      protocolControlledValueUSD
      dailySupplySideRevenueUSD
      cumulativeSupplySideRevenueUSD
      dailyProtocolSideRevenueUSD
      cumulativeProtocolSideRevenueUSD
      dailyTotalRevenueUSD
      cumulativeTotalRevenueUSD
      totalDepositBalanceUSD
      dailyDepositUSD
      cumulativeDepositUSD
      totalBorrowBalanceUSD
      dailyBorrowUSD
      cumulativeBorrowUSD
      dailyLiquidateUSD
      cumulativeLiquidateUSD
      dailyWithdrawUSD
      dailyRepayUSD
    }
  }"""
  url = 'https://api.thegraph.com/subgraphs/name/messari/compound-ethereum'
  r = requests.post(url, json={'query': query})

  # You can parse this data into any form you'd like
  json_data = json.loads(r.text)

  # print(json_data)

  since_id = None
  dataext = json_data #json.loads(result.text)


  # Reformat Twitter's response into nice, flat tables
  financialsDailySnapshots = []
  for t in dataext:
      # Remember the first id we encounter, which is the most recent
      if (since_id == None) :
          since_id = t["id"]

      # Add all financialsDailySnapshots
      financialsDailySnapshots.append({
          "id": t["id"],
          "totalValueLockedUSD": t["totalValueLockedUSD"], #[0]["statusSeverityDescription"],
          "dailySupplySideRevenueUSD" : t["dailySupplySideRevenueUSD"]
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
          "financialsDailySnapshots" : {
              "primary_key" : ["id"]
          }
      },
      "insert": {
          "financialsDailySnapshots": financialsDailySnapshots
      },
      "hasMore" : False
  }
  return ans;
