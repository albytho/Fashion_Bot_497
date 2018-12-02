import React, { Component } from 'react';
import axios from 'axios'
import './App.css';

class App extends Component {

  state = {
    selectedFile: null
  }

  fileSelectedHandler = event => {
    this.setState({
      selectedFile: event.target.files[0]
    })
  }

  fileUploadHandler = () => {
    const fd = new FormData();
    fd.append('file', this.state.selectedFile, this.state.selectedFile.name);

    var config = {
      headers: {'Access-Control-Allow-Origin': '*'}
    };

    axios.post('http://localhost:5000/query/M',fd, config)
      .then(res => {
        console.log(res)
      });
  }

  render() {
    return (
      <div className="App">
        <input type="file" onChange={this.fileSelectedHandler}/>
        <button onClick={this.fileUploadHandler}>Upload</button>
      </div>
    );
  }
}

export default App;
