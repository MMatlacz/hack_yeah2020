import React from "react";
import {Content, List} from "native-base";
import HelpRequestListItem from "./HelpRequestListItem";

class HelpRequestListComponent extends React.Component<HelpRequestListComponentProps> {
    render() {
        return (
            <Content>
                <List>
                    {this.props.requests.map((request) => (
                        <HelpRequestListItem helpRequest={request} key={request.id} navigation={this.props.navigation}>
                        </HelpRequestListItem>
                    ))}
                </List>
            </Content>
        )
    }
}

type HelpRequestListComponentProps = {
    requests: HelpRequest[]
    navigation: any
}

export default HelpRequestListComponent;