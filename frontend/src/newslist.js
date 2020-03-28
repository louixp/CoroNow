import React from "react";
import "./style/news_list.css";
import search_icon from "./resources/search_icon.png";

class Newslist extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      search_text: "",
      item_length: 3
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

  render() {
    var news_data = [
      {
        title: "Title will be here",
        description:
          "This is a demonstration of how description will be displayed on the screen",
        imageUrl: search_icon
      },
      {
        title: "Title will be here",
        description:
          "This is a demonstration of how description will be displayed on the screen",
        imageUrl: search_icon
      },
      {
        title: "Title will be here",
        description:
          "This is a demonstration of how description will be displayed on the screen",
        imageUrl: search_icon
      },
      {
        title: "Title will be here",
        description:
          "This is a demonstration of how description will be displayed on the screen",
        imageUrl: search_icon
      },
      {
        title: "Title will be here",
        description:
          "This is a demonstration of how description will be displayed on the screen",
        imageUrl: search_icon
      },
      {
        title: "Title will be here",
        description:
          "This is a demonstration of how description will be displayed on the screen",
        imageUrl: search_icon
      },
      {
        title: "Title will be here",
        description:
          "This is a demonstration of how description will be displayed on the screen",
        imageUrl: search_icon
      },
      {
        title: "Title will be here",
        description:
          "This is a demonstration of how description will be displayed on the screen",
        imageUrl: search_icon
      },
      {
        title: "Title will be here",
        description:
          "This is a demonstration of how description will be displayed on the screen",
        imageUrl: search_icon
      },
      {
        title: "Title will be here",
        description:
          "This is a demonstration of how description will be displayed on the screen",
        imageUrl: search_icon
      },
      {
        title: "Title will be here",
        description:
          "This is a demonstration of how description will be displayed on the screen",
        imageUrl: search_icon
      },
      {
        title: "Title will be here",
        description:
          "This is a demonstration of how description will be displayed on the screen",
        imageUrl: search_icon
      },
      {
        title: "Title will be here",
        description:
          "This is a demonstration of how description will be displayed on the screen",
        imageUrl: search_icon
      },
      {
        title: "Title will be here",
        description:
          "This is a demonstration of how description will be displayed on the screen",
        imageUrl: search_icon
      },
      {
        title: "Title will be here",
        description:
          "This is a demonstration of how description will be displayed on the screen",
        imageUrl: search_icon
      }
    ];
    var render_list = [];
    if (news_data == []) {
    } else {
      const item_list = news_data.map((item, index) => (
        <Newsitem
          key={index}
          title={item.title}
          description={item.description}
          imageUrl={item.imageUrl}
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
            <div id="search_icon">
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
          <img
            className="news_image"
            src={this.props.imageUrl}
            alt="Not avaliable"
          />
        </div>
        <div className="news_title">{this.props.title}</div>
        <div className="news_desc">{this.props.description}</div>
      </div>
    );
  }
}
export default Newslist;
