import React, { Component } from "react";
import { MDBInput, MDBContainer, MDBBtn, MDBRow, MDBCol } from "mdbreact"; 

import { getRandomSentece, getRandomSentence } from "../utils/requests";

export default class CustomInput extends Component {
    constructor(props) {
        super(props);
        this.state = {
            inputSentence: "",
        }
        this.handleInput = this.handleInput.bind(this);
        this.handleButtonPress = this.handleButtonPress.bind(this);
        this.getRandom = this.getRandom.bind(this);
    }

    handleInput(event) {
        event.preventDefault();
        let input = event.target.value;
        this.setState(
            { inputSentence: input },
            () => console.log(this.state)
        );
    }

    handleButtonPress(event) {
        let pressedButton = event.key;
        if (pressedButton === "Enter" && this.state.inputSentence) {
            console.log(`Submit ${this.state.inputSentence}`);
            this.props.onInput([this.state.inputSentence]);
            this.setState(
                { inputSentence: "" },
                () => console.log("Submitted!")
            );
        }
    }

    getRandom() {
        getRandomSentence().then((sentence) => {
            this.setState(
                { inputSentence: sentence },
                () => console.log(this.state)
            );
        });
    }

    render() {
        return (
            <MDBContainer id="custom-input" className="mb-5">
                <MDBRow>
                    <MDBCol 
                        md="10"
                        className="mx-0"
                    >
                        <MDBInput
                            label="Input your sentence"
                            outline
                            value={this.state.inputSentence}
                            size="lg"
                            onKeyDown={
                                (event) => {
                                    this.handleButtonPress(event);
                                }
                            }
                            onInput={
                                (event) => { 
                                    this.handleInput(event);
                                }
                            }
                        />
                    </MDBCol>
                    <MDBCol 
                        md="2"
                        className="my-auto"
                    >
                        <MDBBtn
                            id="random-btn"
                            color="primary"
                            size="md"
                            onClick={() => this.getRandom()}
                        >
                            Random
                        </MDBBtn>
                    </MDBCol>
                </MDBRow>
            </MDBContainer>
        );
    }
}