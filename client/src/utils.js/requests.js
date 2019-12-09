import axios from "axios";

const URL = "http://0.0.0.0/5000/predict"

function getSentimentPredictions(sentences) {
    return axios({
        method: "post",
        url: URL,
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

export {
    getSentimentPredictions
};