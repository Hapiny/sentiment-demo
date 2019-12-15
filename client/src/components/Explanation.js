import React, { Component } from "react";
import { MDBCollapse, MDBBtn, MDBRow, MDBCol } from "mdbreact";


export default class Explanation extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isOpen: false,
        }
        this.renderFeautres = this.renderFeautres.bind(this);
    }

    renderFeautres() {
        let numNegFeatures = this.props.topNegativeFeauters.length;
        let numPosFeatures = this.props.topPositiveFeauters.length;

        if (numNegFeatures === 0 && numPosFeatures === 0) {
            return null;
        }

        if (numPosFeatures > numNegFeatures) {
            return this.props.topPositiveFeauters.map((feature, idx) => {
                return (
                    <MDBRow>
                        <MDBCol>{feature[0]}{" "}({feature[1]})</MDBCol>
                        <MDBCol>
                            { 
                                idx < numNegFeatures ? 
                                `${this.props.topNegativeFeauters[idx][0]} (${this.props.topNegativeFeauters[idx][1]})` 
                                : null
                            }
                        </MDBCol>
                    </MDBRow>
                );
            })
        } else {
            return this.props.topNegativeFeauters.map((feature, idx) => {
                return (
                    <MDBRow>
                        <MDBCol>
                            { 
                                idx < numPosFeatures ? 
                                `${this.props.topPositiveFeauters[idx][0]} (${this.props.topPositiveFeauters[idx][1]})` 
                                : null
                            }
                        </MDBCol>
                        <MDBCol>{feature[0]}{" "}({feature[1]})</MDBCol>
                    </MDBRow>
                );
            })
        }
    }

    render() {
        return (
            <>
                <MDBBtn
                    size="md"
                    color="primary"
                    onClick={() => this.setState({ isOpen: !this.state.isOpen })}
                >
                    Explanation
                </MDBBtn>
                <MDBCollapse isOpen={this.state.isOpen}>
                    <MDBRow>
                        <MDBCol style={{textDecoration: "underline"}}>Top positive features</MDBCol>
                        <MDBCol style={{textDecoration: "underline"}}>Top negative features</MDBCol>
                    </MDBRow>
                    { this.renderFeautres() }
                </MDBCollapse>
            </>
        );
    }
}