This app is currency convector. It have 4 basic currency code USD, EUR, PLN and CZK.
We may setup this in file: settings/dev-settings.py - <code>CURRENCIES_LIST = ['USD', 'EUR', 'PLN', 'CZK', 'UAH']</code>
<br/>
<p>Run currency exchanger app in terminal:</p>
<code>
  sudo docker-compose up
</code>
<br/>
<p>Create super user for django app:</p>
<code>
  sudo docker-compose run web python3 currency_exchanger/manage.py createsuperuser --settings=settings.dev-settings
</code>
<br/>
> API docs - `http://localhost:8000/api/docs/`<br/>
> Backend - `http://localhost:8000`<br/>
> Frontend - `http://localhost:3000`<br/>

<p>Add rates and curreincies:</p>
  *load data from fixtures -
  <code>
      python3 manage.py loaddata currency rate --settings=settings.dev-settings
  </code>
  OR
  - *Use API:
  ` http://localhost:8000/api/create_all_currencies/` - Creating all currencies which are in list CURRENCIES_LIST.
    and
  ` http://localhost:8000/api/update_rates/` - Creating or updating rates between currencies.
  
*Run tests:
<code>
  sudo docker-compose -f docker-compose.test.yml up
</code>
