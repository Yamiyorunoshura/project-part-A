import yfinance as yf

##McDonald
mcd = yf.Ticker("MCD")
##Coca-cola
ko = yf.Ticker("KO")

snp_price = yf.download("^GSPC",
            start = "2014-10-01",
            end = "2024-09-30")

mcd_price = yf.download("MCD",
            start = "2014-10-01",
            end = "2024-09-30")

ko_price = yf.download("KO",
            start = "2014-10-01",
            end = "2024-09-30")

snp_price2 = snp_price["Adj Close"]
mcd_price2 = mcd_price["Adj Close"]
ko_price2 = ko_price["Adj Close"]

snp_price3 = snp_price2.iloc[:,0]
mcd_price3 = mcd_price2.iloc[:,0]
ko_price3 = ko_price2.iloc[:,0]

snp_price4 = snp_price3.to_list()
mcd_price4 = mcd_price3.to_list()
ko_price4 = ko_price3.to_list()

n_snp = len(snp_price4)
n_mcd = len(mcd_price4)
n_ko = len(ko_price4)

## Calculate the percentage return of S&P
snp_price_new = snp_price4[1:n_snp]
snp_price_old = snp_price4[0:n_snp-1]
snp_return = [(new-old)/old
          for new, old in zip(snp_price_new, snp_price_old)]

mcd_price_new = mcd_price4[1:n_mcd]
mcd_price_old = mcd_price4[0:n_mcd-1]
mcd_return = [(new-old)/old
          for new, old in zip(mcd_price_new, mcd_price_old)]

ko_price_new = ko_price4[1:n_ko]
ko_price_old = ko_price4[0:n_ko-1]
ko_return = [(new-old)/old
          for new, old in zip(ko_price_new, ko_price_old)]