import React, { Component } from 'react';
import { 
    MDBCard, MDBCardBody, MDBCardHeader, 
    MDBInput, MDBBtn, MDBTable, 
    MDBTableBody, MDBTableHead, MDBContainer
} from 'mdbreact';

export default class TablePage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            columns: [
                {
                    'label': 'Model Name',
                    'field': 'model',
                },
                {
                    'label': 'Predicted Label',
                    'field': 'label',
                },
                {
                    'label': [
                        <i className="fa-lg fas fa-smile-beam green-text mr-2"/>,
                        'Positive Prob'
                    ],
                    'field': 'pos_prob'
                },
                {
                    'label': [
                        <i className="fa-lg fas fa-angry red-text mr-2"/>,
                        'Negative Prob'
                    ],
                    'field': 'neg_prob'
                },
                {
                    'label': 'Explanation',
                    'field': 'features'
                }
            ],
            rows: [
                {
                    'model': 'LogisticRegression',
                    'label': 'Positive',
                    'pos_prob': 0.73,
                    'neg_prob': 0.27,
                    'features': <MDBBtn size="sm">Click</MDBBtn>
                },
                {
                    'model': 'NaiveBayes',
                    'label': 'Positive',
                    'pos_prob': 0.61,
                    'neg_prob': 0.39,
                    'features': <MDBBtn size="sm">Click</MDBBtn>
                },
                {
                    'model': 'BaseModel',
                    'label': 'Positive',
                    'pos_prob': 0.5,
                    'neg_prob': 0.5,
                    'features': <MDBBtn size="sm">Click</MDBBtn>
                }
            ]
        }
    }

    render() {
        return (
            <MDBContainer id="result-table">
                <MDBCard narrow>
                    <MDBCardHeader
                        id="table-card" 
                        className="view view-cascade gradient-card-header 
                                blue-gradient d-flex justify-content-between 
                                align-items-center py-2 mx-4"
                    >
                    <div>
                        <MDBBtn outline rounded size="sm" color="white" className="px-2">
                            <i className="fa fa-th-large mt-0"></i>
                        </MDBBtn>
                        <MDBBtn outline rounded size="sm" color="white" className="px-2">
                            <i className="fa fa-columns mt-0"></i>
                        </MDBBtn>
                    </div>
                    
                    <span className="white-text mx-3">Table name</span>
                    <div>
                        <MDBBtn outline rounded size="sm" color="white" className="px-2">
                        <i className="fas fa-pencil-alt mt-0"></i>
                        </MDBBtn>
                        <MDBBtn outline rounded size="sm" color="white" className="px-2">
                        <i className="fas fa-times mt-0"></i>
                        </MDBBtn>
                        <MDBBtn outline rounded size="sm" color="white" className="px-2">
                        <i className="fa fa-info-circle mt-0"></i>
                        </MDBBtn>
                    </div>
                    </MDBCardHeader>
                    <MDBCardBody cascade>
                        <MDBTable>
                            <MDBTableHead columns={this.state.columns} />
                            <MDBTableBody rows={this.state.rows} />
                        </MDBTable>
                    </MDBCardBody>
                </MDBCard>
            </MDBContainer>
        );
    }
}
