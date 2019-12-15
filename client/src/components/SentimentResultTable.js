import React, { Component } from 'react';
import { 
    MDBCard, MDBCardBody, MDBCardHeader, MDBBtn, MDBTable, 
    MDBTableBody, MDBTableHead, MDBContainer
} from 'mdbreact';


export default class TablePage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            columns: [
                {
                    'label': <div className="text-center">
                                <i className="fa-lg fas fa-database mr-2"/>
                                <span style={{fontWeight: "bold"}}>Model</span>
                             </div>,
                    'field': 'model',
                },
                {
                    'label': <div className="text-center">
                                <i className="fa-lg fas fa-tag blue-text mr-2"/>
                                <span style={{fontWeight: "bold"}}>Label</span>
                             </div>,
                    'field': 'label',
                },
                {
                    'label': <div className="text-center">
                                <i className="fa-lg fas fa-smile-beam green-text mr-2"/>
                                <span style={{fontWeight: "bold"}}>Positive Prob</span>
                             </div>,
                    'field': 'pos_prob'
                },
                {
                    'label': <div className="text-center">
                                <i className="fa-lg fas fa-angry red-text mr-2"/>
                                <span style={{fontWeight: "bold"}}>Negative Prob</span>
                             </div>,
                    'field': 'neg_prob'
                },
                {
                    'label': <div className="text-center">
                                <i className="fa-lg fas fa-magic orange-text mr-2"/>
                                <span style={{fontWeight: "bold"}}>Explanation</span>
                             </div>,
                    'field': 'features'
                }
            ],
        }
    }

    render() {
        return (
            <MDBContainer id="result-table">
                <MDBCard narrow>
                    <MDBCardHeader
                        id="table-card" 
                        style={{
                            backgroundColor: "#2e2e2e",
                            borderRadius: "10px"
                        }}
                        className="view view-cascade mx-4"
                    >
                        <h3 className="mx-5 white-text">
                            {
                                this.props.sentence
                            }
                        </h3>
                    </MDBCardHeader>
                    <MDBCardBody cascade>
                        <MDBTable>
                            <MDBTableHead 
                                columns={this.state.columns} 
                                
                            />
                            <MDBTableBody 
                                rows={this.props.rows} 
                            />
                        </MDBTable>
                    </MDBCardBody>
                </MDBCard>
            </MDBContainer>
        );
    }
}