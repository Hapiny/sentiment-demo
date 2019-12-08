import React, { Component } from "react";
import { 
    MDBNavbar, MDBNavbarBrand,
    MDBNavbarNav, 
} from "mdbreact";


export default class Navbar extends Component {
    render() {
        return (    
            <MDBNavbar id="navbar" className="heavy-rain-gradient" left={"true"}>
                <lottie-player
                    id="logo"
                    src="https://assets3.lottiefiles.com/packages/lf20_DsCKSA/unicorn 2.json"
                    background="transparent" 
                    speed="1"
                    loop autoplay >
                </lottie-player>

                <MDBNavbarNav left>
                    <MDBNavbarBrand className="nav-text">
                        <strong>
                            Sentiment Classification
                        </strong>
                    </MDBNavbarBrand>
                </MDBNavbarNav>
            </MDBNavbar>
            );
    }
}
