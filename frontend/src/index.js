import React from 'react';
import ReactDOM from 'react-dom';
import Websocket from 'react-websocket';
import './index.css';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useRouteMatch,
  useParams
} from "react-router-dom";

  class TourGame extends React.Component {
    constructor(props){
      super(props)
      this.state = {
        participants: [{"name": "Chris", "icon": "bla.png"}, {"name": "Maxi", "icon": "bla2.png"}],
        beerStats: {
          "Chris": [
            {
              "size" : 500,
            }
          ]
        },
      }
    }
    
    handleData(data) {
      let result = JSON.parse(data);
      this.setState({participants: result.participants, beerStats: result.beerStats});
    }
    
    render(){
      return(
        <TrinkerListe participants = {this.state.participants}/>
        /*<BierStats />,
        <WohnzimmerFahrt />,
        <Fragespiel />,
        <Reaktionsbutton />,
        <div>
          Count: <strong>{this.state.count}</strong>
 
          <Websocket url='ws://localhost:8888/live/product/12345/'
              onMessage={this.handleData.bind(this)}/>
        </div>*/
      )
    }
  }

  class TrinkerListe extends React.Component {

    render() {
      return (
        <div className="trinkerListe">
          <ul>
              {this.createList()}
          </ul>
        </div>
      );
    }

    createList (){
      let list = []
      for(let user in this.props.participants) {
          list.push(<TrinkerElement  trinkerDetails={this.props.participants[user]} key={user}/>)
      }
      return list
    }

    addTrinker(){
      var newArray = this.props.participants.slice();
      newArray.push("new value");
      this.setState({participants:newArray})
      console.log(this.props.participants)
    }
  }

  class TrinkerElement extends React.Component {
    render () {
      return(
        <li className="trinker"> {this.props.trinkerDetails.name} </li>
      )
    }
  }

  class RouterWrapper extends React.Component {
    render() {
      return(
        <Router>
          <div>
            <nav>
              <ul>
                <li>
                  <Link to="/">Login</Link>
                </li>
                <li>
                  <Link to="/game">Game</Link>
                </li>
              </ul>
            </nav>

            {/* A <Switch> looks through its children <Route>s and
                renders the first one that matches the current URL. */}
            <Switch>
              <Route path="/">
                <Login />
              </Route>
              <Route path="/game">
                <TourGame />
              </Route>
            </Switch>
          </div>
        </Router>
      )
    }
  }

  class Login extends React.Component {
    constructor(props) {
      super(props);
      this.state = {loginName: ''};
      this.handleChange = this.handleChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
      this.setState({loginName: event.target.value});
    }
    
    handleSubmit(event) {
      var nameToSend = this.state.loginName
      fetch('mileservice/its_me/' + encodeURIComponent(nameToSend), {//@todo chris url testen
        method: 'POST',
        dataType: 'json',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(nameToSend),
      })
      .then(response => response.json())
      .then(response => {console.log(response)})
      event.preventDefault();
    }
    
    render() {
      return(
        <div className="loginField">
          <h2>Login</h2>
          <form onSubmit={this.handleSubmit}>
            <label>
              Name:
              <input type="text" value={this.state.loginName} onChange={this.handleChange} />
            </label>
            <input type="submit" value="Submit" />
          </form>
        </div>
      )
    }
  }
  // ========================================
  
  ReactDOM.render(
    <RouterWrapper />,
    document.getElementById('root')
  );
  