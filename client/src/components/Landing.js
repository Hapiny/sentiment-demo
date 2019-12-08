import React, { Component } from 'react';

import CustomInput from "./CustomInput";
import TablePage from "./SentimentResultTable";

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
                <h2 className=" mt-5 text-center">
                    You can run your models on custom sentence.
                </h2>
                <CustomInput
                    onInput={
                        (input) => {
                            this.setState(
                                { modelInputs: [input] },
                                () => console.log(this.state)
                            );
                        }
                    }
                />
                <TablePage />
            </div>
        );
    }
}