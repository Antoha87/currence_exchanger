This app is currency convector. It have 4 basic currency code USD, EUR, PLN and CZK.
We may setup this in file: <code>settings/dev-settings.py - CURRENCIES_LIST = ['USD', 'EUR', 'PLN', 'CZK', 'UAH']</code>

**Run currency exchanger app in terminal:**
<code>
  sudo docker-compose up
</code>

**Create super user for django app:**
<code>
  sudo docker-compose run web python3 currency_exchanger/manage.py createsuperuser --settings=settings.dev-settings
</code>

 **API docs** - `http://localhost:8000/api/docs/`<br/>
 **Backend** - `http://localhost:8000`<br/>
 **Frontend** - `http://localhost:3000`<br/>

**Add rates and curreincies:**
  1) Load data from fixtures:
  <code>
      python3 manage.py loaddata currency rate --settings=settings.dev-settings
  </code>
  2) Use API:<br/>
  http://localhost:8000/api/create_all_currencies/ - **Creating all currencies which are in** <code>CURRENCIES_LIST</code>.
  http://localhost:8000/api/update_rates/ - **Creating or updating rates between currencies**.<br/>
  
**Run tests:**<br/>
<code>
  sudo docker-compose -f docker-compose.test.yml up
</code>
