import {Left, Thumbnail, View} from "native-base";
import React from "react";

const mask1 =require('../../../imgs/mask-1.png');
const mask2 =require('../../../imgs/mask-2.png');
const masks = [mask1, mask2];

const getMaskForRequest = (request: HelpRequest) => {
    const number = parseInt(request.id.slice(0, 4), 16);
    return masks[number % masks.length]
}


class HelpRequestAvatar extends React.Component<HelpRequestAvatarProps> {
    render() {
        return (
            <View style={{height: 25}}>
                <Thumbnail source={{uri: `http://api.adorable.io/avatar/256/${this.props.helpRequest.full_name}`}} />
                <Thumbnail source={getMaskForRequest(this.props.helpRequest)} style={{position:"absolute", top: "60%"}}/>
            </View>
        )
    }
}

type HelpRequestAvatarProps = {
    helpRequest: HelpRequest
};

export default HelpRequestAvatar;
