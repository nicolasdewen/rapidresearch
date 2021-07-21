import os
from flask import Flask, flash, redirect, render_template, request, session
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO


from apiinfo import profile, ratios, metrics, isgrowth, ratings, news, prices, gainers, losers, actives, sectors
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Make sure API key is set
if not os.environ.get("FMP_API_KEY"):
    raise RuntimeError("FMP_API_KEY not set")

@app.route("/")
def index():
    # Load most actives, gainers, losers and sector data for landing page
    gainer = gainers()[0:5]
    loser = losers()[0:5]
    active = actives()[0:5]
    sector = sectors()
    date = sector[0]["date"]
    date1 = sector[1]["date"]
    date2 = sector[2]["date"]
    sector = sector[0:3]
    # Convert to %
    for month in sector:
        del month["date"]
        for k,v in month.items():
            if v != None and v != 0:
                month[k] = str(round(v, 2)) + "%"

    return render_template("index.html", gainer=gainer, loser=loser, active=active, sector=sector, date=date, date1=date1, date2=date2)

@app.route("/reports", methods=["GET", "POST"])
def reports():
    # If submitting
    if request.method == "POST":
        # Get ticker
        ticker = request.form.get("ticker")
        if not ticker:
            return render_template("reports.html")
        ticker = ticker.upper()

        # Get profile as list
        prof = profile(ticker)

        # Ensure data has been downloaded
        if not prof:
            return render_template("reports.html")
        else:
            prof = prof[0]
            # Format market cap
            mktCap = prof["mktCap"]
            mktCap = f'{mktCap:,}'

        # Get rating
        rating = ratings(ticker)
        if not rating:
            return render_template("reports.html")
        rating = rating[0]
        rate = rating["ratingRecommendation"]

        # Get ratios as list
        ratio = ratios(ticker)
        if not ratio:
            return render_template("reports.html")
        else:
            ratio = ratio[-1]

            # Round ROE, ROA, Div Yield, PE, PB, DE, GPM, OPM, INVTO, INTCOV and convert to percentages
            roe = ratio["returnOnEquityTTM"]
            roe = round(roe*100, 2)
            roa = ratio["returnOnAssetsTTM"]
            roa = round(roa*100, 2)
            div = ratio["dividendYielPercentageTTM"]
            if div:
                div = round(div, 2)
            pb = ratio["priceToBookRatioTTM"]
            pb = round(pb, 2)
            de = ratio["debtEquityRatioTTM"]
            de = round(de, 2)
            gpm = ratio["grossProfitMarginTTM"]
            gpm = round(gpm*100, 2)
            opm = ratio["operatingProfitMarginTTM"]
            opm = round(opm*100, 2)
            invto = ratio["inventoryTurnoverTTM"]
            if invto:
                invto = round(invto, 2)
            intcov = ratio["interestCoverageTTM"]
            if intcov:
                intcov= round(intcov, 2)

            # PE > 300, rating = Sell
            pe = ratio["priceEarningsRatioTTM"]
            pe = round(pe, 2)
            if int(pe) >= 300:
                rate = "SELL"

        # Get financial metrics
        metric = metrics(ticker)
        if not metric:
            return render_template("reports.html")
        else:
            metric = metric[-1]
            eveb = metric["enterpriseValueOverEBITDATTM"]
            eveb = round(eveb, 2)
            payoutratio = metric["payoutRatioTTM"]
            if payoutratio:
                payoutratio = round(payoutratio*100, 2)
            roic = metric["roicTTM"]
            roic = round(roic*100, 2)

            if roic == 0:
                valcreate = ""

            if roic < 2 and roic > 0:
                valcreate = "Given the level of return on invested capital, it appears the company is destroying value"

            if roic > 2 and roic < 10:
                valcreate = "Given the level of return on invested capital, it appears the company is healthy and growing, effectively creating value."

            if roic > 10:
                valcreate = "The exceptional rate of return on invested capital is evidence of a great deal of value creation and provides an indicator for the growth prosects and overall health of the company."

        # Income statement growth figures
        pl = isgrowth(ticker)
        if not pl:
            return render_template("reports.html")

        # Avg Revenue and R&D growth, append none values to avoid errors
        avgrnd = 0
        avgrev = 0
        if len(pl) >= 3:
            for i in range(3):
                avgrnd += (pl[i]["growthResearchAndDevelopmentExpenses"])/3
                avgrev += (pl[i]["growthRevenue"])/3

        if len(pl) == 2:
            temp_dict = {}
            temp_dict["growthResearchAndDevelopmentExpenses"] = None
            temp_dict["growthRevenue"] = None
            temp_dict["date"] = int((pl[0]["date"])[:4]) - 1
            pl.append(temp_dict)
            for i in range(2):
                avgrnd += (pl[i]["growthResearchAndDevelopmentExpenses"])/2
                avgrev += (pl[i]["growthRevenue"])/2

        if len(pl) == 1:
            temp_dict = {}
            temp_dict["growthResearchAndDevelopmentExpenses"] = None
            temp_dict["growthRevenue"] = None
            for i in range(2):
                temp_dict["date"] = int((pl[0]["date"])[:4]) - i
                pl.append(temp_dict)

            avgrnd += (pl[i]["growthResearchAndDevelopmentExpenses"])
            avgrev += (pl[i]["growthRevenue"])

        avgrev = round(avgrev*100, 2)
        avgrnd = round(avgrnd*100, 2)

        # Get news
        new = news(ticker)
        if not new:
            return render_template("reports.html")
        else:
            new = new[:10]

        # Plot price action
        listofdf = []
        price = prices(ticker)
        if not price:
            return render_template("reports.html")
        # Get last 600 days prices
        price = price['historical'][600:0:-1]
        # Pandas dataframe
        pricedf = pd.DataFrame.from_dict(price)
        # Rename column from close to ticker
        pricedf = pricedf.rename({'close': ticker}, axis=1)
        listofdf.append(pricedf)

        dfs = [df.set_index("date") for df in listofdf]
        priceconcat = pd.concat(dfs, axis=1)

        fig = plt.figure()
        for i, col in enumerate(priceconcat.columns):
            priceconcat[col].plot()

        # Design plot
        plt.title('Price Action')
        plt.xticks(rotation=70)
        plt.legend(priceconcat.columns)
        plt.tight_layout()
        ax = plt.gca()
        ax.set_facecolor("black")

        # Encode plot with base64
        tmpfile = BytesIO()
        fig.savefig(tmpfile, format="png")
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

        return render_template("reports2.html", prof=prof, rate=rate, mktCap=mktCap, ratio=ratio, roe=roe, roa=roa, metric=metric,
        pl=pl, avgrnd=avgrnd, avgrev=avgrev, new=new, encoded=encoded, pe=pe, div=div, pb=pb, de=de, eveb=eveb, gpm=gpm, opm=opm,
        invto=invto, intcov=intcov, payoutratio=payoutratio, roic=roic, valcreate=valcreate)

    # If loading page
    return render_template("reports.html")

@app.route("/info")
def info():
    return render_template("info.html")