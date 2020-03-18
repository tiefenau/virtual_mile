import React from 'react';
import ReactDOM from 'react-dom';
import Websocket from 'react-websocket';
import './index.css';

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
    constructor(props){
      super(props)  
    }

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

  // ========================================
  
  ReactDOM.render(
    <TourGame />,
    document.getElementById('root')
  );
  