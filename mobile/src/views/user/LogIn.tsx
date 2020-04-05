import {Body, Container, Footer, Form, FooterTab, Header, Text, Title, Button, Content, Item, Input, Label} from "native-base";
import React from "react";


export default class LogIn extends React.Component {
    render = () => {
        return (
            <Container>
                <Header>
                    <Body>
                        <Title>Login</Title>
                    </Body>
                </Header>
                <Content>
                    <Form>
                        <Item floatingLabel>
                            <Label>Email</Label>
                            <Input
                                autoCapitalize="none"
                                placeholder="Email"
                                autoCompleteType="email"
                                keyboardType="email-address"
                                textContentType="emailAddress"
                                onChangeText={email => this.setState({ email })}
                            />
                        </Item>
                        <Item floatingLabel last>
                            <Label>Password</Label>
                            <Input
                                secureTextEntry={true}
                                placeholder="Password"
                                autoCompleteType="password"
                                onChangeText={password => this.setState({ password })}
                            />
                        </Item>
                    </Form>
                    <Button
                        onPress={ () => {this.props.userSerivice.logIn(this.state.email, this.state.password)}}
                        style={{marginTop: 20}}

                    >
                        <Text> LogIn </Text>
                    </Button>
                </Content>
                <Footer>
                    <FooterTab>
                        <Button active={false} onPress={() => { }}>
                            <Text>Login</Text>
                        </Button>
                    </FooterTab>
                    <FooterTab>
                        <Button active={true} onPress={() => {}} >
                            <Text>Register</Text>
                        </Button>
                    </FooterTab>
                </Footer>
            </Container>
        )
    };
}