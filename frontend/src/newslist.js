import React from "react";
import "./style/news_list.css";
import search_icon from "./resources/search_icon.png";

class Newslist extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      search_text: "",
      item_length: 3,
      news_data: []
    };
  }

  dynamic_resize() {
    var innerWidth = window.innerWidth;
    console.log(innerWidth);
    for (let i = 0; i < 7; i++) {
      if (innerWidth < (i + 1) * 300 && innerWidth >= i * 300)
        this.setState({
          item_length: Math.max(i, 1)
        });
    }
  }

  componentWillMount() {
    this.dynamic_resize();
    window.addEventListener("resize", this.dynamic_resize.bind(this));
    window.addEventListener("fullscreenchange", this.dynamic_resize.bind(this));
  }

  update_text(e) {
    this.setState({
      search_text: e.target.value
    });
  }

  async search() {
    var esc = encodeURIComponent;
    var url = "/news_list" + "?question=" + esc(this.state.search_text);
    await fetch(url, {
      method: "GET",
      cache: "no-cache",
      headers: {
        "Content-type": "application/json"
      },
      redirect: "follow"
    })
      .then(res => res.json())
      .then(res => {
        this.setState({
          news_data: res
        });
      });
  }

  render() {
    var news_data = this.state.news_data;
    var render_list = [];
    if (news_data == []) {
      console.log("here");
      render_list = <div id="error_msg">No Result Found</div>;
    } else {
      const item_list = news_data.map((item, index) => (
        <Newsitem
          key={index}
          title={item.title}
          description={item.description}
          imageUrl={item.urlToImage}
          url={item.url}
        />
      ));
      for (let i = 0; i < item_list.length; i += this.state.item_length) {
        var row_items = [];
        for (
          let j = i;
          j < Math.min(i + this.state.item_length, item_list.length);
          j++
        )
          row_items.push(item_list[j]);
        render_list.push(<div className="item_row">{row_items}</div>);
      }
    }
    return (
      <div id="news_list">
        <div id="search_div">
          <div className="font-effect-3d" id="search_title">
            Search for Coronavirus News
          </div>
          <div id="search_bar">
            <input
              type="text"
              id="search_input"
              value={this.state.search_text}
              onChange={this.update_text.bind(this)}
            />
            <div id="search_icon" onClick={this.search.bind(this)}>
              <img src={search_icon} alt="Search" />
            </div>
          </div>
        </div>
        <div id="content_div">{render_list}</div>
      </div>
    );
  }
}

class Newsitem extends React.Component {
  render() {
    return (
      <div className="news_items">
        <div className="news_frame">
          <a href={this.props.url}>
            <img
              className="news_image"
              src={this.props.imageUrl}
              alt="Not avaliable"
            />
          </a>
        </div>
        <div className="news_title">
          <p>{this.props.title}</p>
        </div>
        <div className="news_desc">
          <p>{this.props.description}</p>
        </div>
      </div>
    );
  }
}
export default Newslist;
