import React from "react";
import {ListItem, Text, Left, Body, Right, List, View, H3, Tab,Tabs, Button} from "native-base";
import HelpRequestAvatar from "../common/HelpRequestAvatar";
import HelpRequestsServiceContext from "../../../contexts/helpRequestsService";
import HelpRequestProducts from "../common/HelpRequestProducts";


class HelpRequestExpandedBody extends React.Component<HelpListItemProps> {
    static contextType = HelpRequestsServiceContext;

    constructor(props) {
        super(props);
        this.takeHelpRequest = this.takeHelpRequest.bind(this);
    }

    takeHelpRequest() {
        const navigation = this.props.navigation;
        this.context.assignForHelp(this.props.helpRequest.id).then(() => {
            navigation.navigate("HelpSummary", {requestID: this.props.helpRequest.id});
        });
    }

    render() {
        const flexItemStyle = {
            flexGrow: 2,
        }
        return (
            <View >
                <View style={{margin: 10}}>
                    <HelpRequestProducts helpRequest={this.props.helpRequest}/>
                </View>
                <View style={{margin: 10}}>
                    <H3>Czas odbioru</H3>
                    <Text> { this.props.helpRequest.pickup_time }</Text>
                </View>
                <View style={{flex: 1, flexDirection: "row", justifyContent: "space-around"}}>
                    <Button style={flexItemStyle} onPress={this.takeHelpRequest}>
                        <Text style={{textAlign: 'center'}}>Robię zakupy!</Text>
                    </Button>
                </View>
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
                    { this.state.isExpanded ? <HelpRequestExpandedBody {... this.props} /> : null }
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
    navigation: any
}



export default HelpRequestListItem;