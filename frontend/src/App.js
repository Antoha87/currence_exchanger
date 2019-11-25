import React, {Component} from 'react';


class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            currencies: [{code: "------", id: 0}],
            fromCurrency: 1,
            toCurrency: 1,
            amount: 0,
            totalAmount: 0,
            rate: 0,
            isLoaded: false,

        };
        this.handleChange = this.handleChange.bind(this);
        this.getRate = this.getRate.bind(this);
    }


    handleChange(event) {
        const target = event.target;
        const name = target.name;

        this.setState({
            [name]: target.value
        });
    }


    componentDidMount() {
        fetch("http://localhost:8000/api/currencies/?format=json")
            .then(res => res.json())
            .then(res => {
                this.setState({
                    currencies: [...this.state.currencies, ...res],
                    isLoaded: true
                });
            })
            .catch(error => {
                console.log(error)
            })
    }


    getRate() {
        const url = new URL("http://localhost:8000/api/rate"),
            params = {
                from_currency: this.state.fromCurrency,
                to_currency: this.state.toCurrency,
                amount: this.state.amount
            };
        Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));

        fetch(url)
            .then((response) => {
                return response.json()
            })
            .then((data) => {
                this.setState({
                    rate: data.rate
                });
                this.setState({
                    totalAmount: data.total_amount
                })
            })

    }

    render() {
        let total = this.state.totalAmount;
        let rate = this.state.rate;


        return (
            <div className='container'>
                <div className="row">
                    <div className="App">
                        <header className="App-header">
                            <h1>
                                Currency Exchanger
                            </h1>
                        </header>

                        <div className="form-block">
                            <div className="input-group mb-3">
                                <div className="input-group-prepend">
                                    <span className="input-group-text" id="basic-addon1">@</span>
                                </div>
                                <input type="text" placeholder="Amount" aria-label="Amount"
                                       aria-describedby="basic-addon1" className="form-control" name="amount"
                                       onChange={this.handleChange}/>
                            </div>

                            <div className="input-group mb-3">
                                <div className="input-group-prepend">
                                    <label className="input-group-text" htmlFor="inputGroupSelect01"
                                           to="fromCurrency"><b>From</b></label>
                                    <select className="custom-select" id="inputGroupSelect01" name="fromCurrency"
                                            onChange={this.handleChange}>
                                        {this.state.currencies.map((curr) =>
                                            <option value={curr.id} key={curr.id}>{curr.code}</option>
                                        )}
                                    </select>

                                    <label className="input-group-text" htmlFor="inputGroupSelect02"
                                           to="toCurrency"><b>To</b></label>
                                    <select className="custom-select" id="inputGroupSelect01" name="toCurrency"
                                            onChange={this.handleChange}>
                                        {this.state.currencies.map((curr) =>
                                            <option value={curr.id} key={curr.id}>{curr.code}</option>
                                        )}
                                    </select>

                                </div>
                            </div>
                        </div>
                        <div className="row">
                            <div className="col">
                                <div className="alert alert-success" role="alert">
                                    Rate - {rate}
                                </div>
                                <div className="alert alert-success" role="alert">
                                    Total Amount - {total}
                                </div>

                            </div>
                        </div>
                        <button className="btn btn-outline-success" onClick={this.getRate}>Convert</button>
                    </div>
                </div>
            </div>
        );
    }
}

export default App;
