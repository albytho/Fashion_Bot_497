import React, { Component } from 'react';
import './App.css';

class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      query_results : []
    };
  }

  compontDidMount(){

  }

  handleUploadImage(ev) {
    ev.preventDefault();

    let data = new FormData();
    data.append('file', this.uploadInput.files[0]);

    fetch('http://localhost:5000/query/M', {
      method: 'POST',
      body: data,
    }).then((response) => {
      response.json().then((body) => {
        console.log("IT WORKED");
      });
    });
  }

  render() {
    return (
      <div className="App">
        <form onSubmit={this.handleUploadImage}>
          <div>
            <input ref={(ref) => { this.uploadInput = ref; }} type="file" />
          </div>
          <br />
          <div>
            <button>Upload</button>
          </div>
        </form>
      </div>
    );
  }
}

export default App;
