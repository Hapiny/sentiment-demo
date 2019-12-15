import React, { Component } from 'react';

import CustomInput from "./CustomInput";
import TablePage from "./SentimentResultTable";
import Explanation from "./Explanation";

import { getSentimentPredictions } from "../utils/requests";

export default class Landing extends Component {
    constructor(props) {
        super(props);
        this.state = {
            modelInputs: [],
            modelOutputs: []
        }
        this.processResponse = this.processResponse.bind(this);
    }

    processResponse() {
        return this.state.modelOutputs.map((elem) => {
            let response = elem.response[0]
            return {
                "model": <div className="text-center">
                            {elem.model}
                         </div>,
                "label": <div className="text-center">
                            {response.label === "pos" ? "Positive" : "Negative"}
                         </div>,
                "pos_prob": <div className="text-center">
                                {response.pos_prob}
                            </div>,
                "neg_prob": <div className="text-center">
                                {response.neg_prob}
                            </div>,
                "features": <div className="text-center">
                                <Explanation
                                    topNegativeFeauters={response.neg_features}
                                    topPositiveFeauters={response.pos_features}
                                />
                            </div>
            }
        })
    }

    render() {
        return (
            <div>
                <h2 className=" mt-5 text-center">
                    You can run your models on custom sentence.
                </h2>
                <CustomInput
                    onInput={
                        (inputs) => {
                            this.setState(
                                { modelInputs: inputs },
                                () => { 
                                    console.log(this.state.modelInputs);
                                    getSentimentPredictions(this.state.modelInputs).then(
                                        (response) => {
                                            this.setState(
                                                { modelOutputs: response },
                                                () => { 
                                                    console.log("Success!");
                                                    console.log(this.state.modelOutputs);
                                                }
                                            );
                                        }
                                    )
                                }
                            );
                        }
                    }
                />
                { 
                    this.state.modelOutputs.length === 0 ? null: 
                    <TablePage 
                        rows={this.processResponse()}
                        sentence={this.state.modelInputs[0]}
                    />
                }
            </div>
        );
    }
}