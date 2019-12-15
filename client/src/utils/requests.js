import axios from "axios";

const PRED_REQ = "http://83.149.198.198:5000/predict"
const RND_REQ = "http://83.149.198.198:5000/random"

function getSentimentPredictions(sentences) {
    return axios({
        method: "post",
        url: PRED_REQ,
        data: {
            "data": sentences
        },
        headers: { 
            'Content-type': 'application/json' 
        }
    }).then(response => {
        console.log("Request: OK")
        return response.data;
    }).catch(error => {
        console.log("Request: Error")
        console.log(error);
    });
}

function getRandomSentence() {
    return axios({
        method: "get",
        url: RND_REQ,
        headers: { 
            'Content-type': 'application/json' 
        }
    }).then(response => {
        console.log("Request: OK")
        return response.data;
    }).catch(error => {
        console.log("Request: Error")
        console.log(error);
    });
}

export {
    getSentimentPredictions,
    getRandomSentence
};