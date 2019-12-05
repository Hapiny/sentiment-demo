import React, { Component } from 'react';

import CustomInput from "./CustomInput";

export default class Landing extends Component {
    constructor(props) {
        super(props);
        this.state = {
            modelInputs: [],
        }
    }

    render() {
        return (
            <div>
                <p className="lead my-5 text-center">
                    You can run your models on custom sentence.
                </p>
                {
                    this.props.appMode === "custom" ?
                        <CustomInput
                            onInput={
                                (input) => {
                                    this.setState(
                                        { modelInputs: [input] },
                                        () => console.log(this.state)
                                    );
                                }
                            }
                        /> : 
                        null
                }
            </div>
        );
    }
}