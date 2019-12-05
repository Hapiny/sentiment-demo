import React, { Component } from "react";
import { 
    MDBNavbar, MDBNavbarBrand,
    MDBNavbarNav, 
    // MDBBtn, MDBRow, MDBNavItem
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
                {/* <MDBNavbarNav left>
                    <MDBRow className="ml-5">
                        <MDBNavItem className="mr-2">
                            <MDBBtn 
                                className="rainy-ashville-gradient" 
                                style={{color: "rgb(63, 62, 62)", fontWeight: "bold"}}
                                onClick={() => this.props.handler("custom")}
                            >
                                Custom sentence
                            </MDBBtn>
                        </MDBNavItem>

                        <MDBNavItem>
                            <MDBBtn 
                                className="deep-blue-gradient"
                                style={{color: "rgb(63, 62, 62)", fontWeight: "bold"}}
                                onClick={() => this.props.handler("random")}
                            >
                                Random samples
                            </MDBBtn>
                        </MDBNavItem>
                    </MDBRow>
                </MDBNavbarNav> */}
            </MDBNavbar>
            );
    }
}
