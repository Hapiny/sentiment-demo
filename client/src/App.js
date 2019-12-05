import React, { Component } from 'react';
import Navbar from './components/Navbar';
import Landing from './components/Landing';


export default class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            mode: "custom",
        }
    }


    render() {
        return ([
            <Navbar 
                key="navbar" 
                // handler={
                //     (newMode) => {
                //         this.setState(
                //             { mode: newMode }, 
                //             () => console.log(this.state)
                //         )
                //     }
                // }
            />,
            <Landing 
                key="landing"
                appMode={this.state.mode}
            />
        ]);    
    }
}
