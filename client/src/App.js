import React, { Component } from 'react';
import Navbar from './components/Navbar';
import Landing from './components/Landing';


export default class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            
        }
    }


    render() {
        return ([
            <Navbar
                key="navbar" 
            />,
            <Landing 
                key="landing"
            />
        ]);    
    }
}
