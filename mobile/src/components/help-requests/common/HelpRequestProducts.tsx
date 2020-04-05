import {View, H3, List, ListItem, Text, CheckBox, Right, Left} from "native-base";
import React from "react";

class HelpRequestProducts extends React.Component<HelpRequestProductsProps> {
    render() {
        return <View>
            <H3>Lista zakupów</H3>
            <List>
                { this.props.helpRequest.products.map((product) => {
                   return (
                       <ListItem key={product}>
                            <Left>
                                <Text>{product}</Text>
                            </Left>
                           { this.props.checkBox? <Right><DummyCheckBox/></Right> : null }
                        </ListItem>
                   )
                })}
            </List>
        </View>
    }
}

class DummyCheckBox extends React.Component {
    constructor(props) {
        super(props);
        this.state = {checked: false}
    }

    render() {
        return (
            <CheckBox checked={this.state.checked} onPress={()=> {this.setState({checked: !this.state.checked})}}/>
        )
    }
}

type HelpRequestProductsProps = {
    helpRequest: HelpRequest
    checkBox?: boolean
}

export default HelpRequestProducts;