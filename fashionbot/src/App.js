import React, { Component } from 'react';
import axios from 'axios'
import './App.css';

class App extends Component {

  state = {
    selectedFile: null,
    results: [],
    gender: 'X',
    minMoney: 0,
    maxMoney: 100000
  }

  handleGenderChange = event => {
    this.setState({
      gender: event.target.value
    })
  }

  handleMinMoneyChange = event => {
    this.setState({
      minMoney: event.target.value
    })
  }

  handleMaxMoneyChange = event => {
    this.setState({
      maxMoney: event.target.value
    })
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

    let url = 'http://localhost:5000/query/'.concat(this.state.gender)
    url = url.concat('/')
    url = url.concat(this.state.minMoney)
    url = url.concat('/')
    url = url.concat(this.state.maxMoney)

    axios.post(url, fd, config)
      .then(res => {
        console.log(res)
        this.setState({
          results: res.data.results
        })
      });
  }

  render() {
    return (
      <div className="App">
        <input type="file" onChange={this.fileSelectedHandler}/>

        <select value={this.state.gender} onChange={this.handleGenderChange}>
          <option value="M">Male</option>
          <option value="F">Female</option>
          <option value="X">Either</option>
        </select>

        <input type="number" placeholder="Min Budget" onChange={this.handleMinMoneyChange}/>
        <input type="number" placeholder="Max Budget" onChange={this.handleMaxMoneyChange}/>

        <button onClick={this.fileUploadHandler}>Upload</button>
      {this.state.results.map(item =>
        (<div>
          <a href={item.url}>
            <img src={item.images} alt="pic"/>
          </a>
          {item.price}
          {item.product_brand}
          {item.product_name}
        </div>),
      )}
      </div>
    );
  }
}

export default App;
