import React from "react";
import {ListItem, Text, Left, Body, Right, List, View} from "native-base";
import HelpRequestAvatar from "../common/HelpRequestAvatar";


class HelpRequestExpandedBody extends React.Component<HelpListItemProps> {
    render() {
        return (
            <View>
                <Text> List zakupów:</Text>
                <List>
                    { this.props.helpRequest.products.map((product) => (
                        <ListItem><Text>{product}</Text></ListItem>
                    ))}
                </List>
            </View>
        );
    }
}


class HelpRequestListItem extends React.Component<HelpListItemProps> {
    constructor(props: HelpListItemProps) {
        super(props);
        this.state = {
            isExpanded: false
        }
        this.expandItem = this.expandItem.bind(this);
    }

    expandItem() {
        this.setState({isExpanded: !this.state.isExpanded})
    }

    render() {
        return (
            <ListItem avatar selected={this.state.isExpanded} onPress={this.expandItem}>
                <Left>
                    <HelpRequestAvatar helpRequest={this.props.helpRequest}/>
                </Left>
                <Body>
                    <Text>{this.props.helpRequest.full_name}</Text>
                    <Text note> {this.props.helpRequest.address.address} </Text>
                    { this.state.isExpanded ? <HelpRequestExpandedBody helpRequest={this.props.helpRequest}/> : null }
                </Body>
                <Right>
                    <Text note>{this.props.helpRequest.created_at.getHours()}:{this.props.helpRequest.created_at.getMinutes()}</Text>
                </Right>
            </ListItem>
        );
    }
}



type HelpListItemProps = {
    helpRequest: HelpRequest
}



export default HelpRequestListItem;