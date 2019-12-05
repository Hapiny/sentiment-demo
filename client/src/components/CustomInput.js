import React, { Component } from "react";
import { MDBInput, MDBContainer } from "mdbreact"; 

export default class CustomInput extends Component {
    constructor(props) {
        super(props);
        this.state = {
            inputSentence: "",
        }
        this.handleInput = this.handleInput.bind(this);
        this.handleButtonPress = this.handleButtonPress.bind(this);
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
            this.props.onInput(this.state.inputSentence);
            this.setState(
                { inputSentence: "" },
                () => console.log("Submitted!")
            );
        }
    }

    render() {
        return (
            <MDBContainer id="custom-input">
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
            </MDBContainer>
        );
    }
}