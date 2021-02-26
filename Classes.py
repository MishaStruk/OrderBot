FOODDICT={"pizza": 0, "toast":1, "falafel":2}


class user_in_registration:
    def __init__(self,userid):
        self.id = userid
        self.pass1 = None
        self.pass2 = None
    def check_passwords(self):
        if(self.pass1 == self.pass2 and self.pass1 != None):
            return True
    def get_details(self):
        return self.id,self.pass1
    def get_id(self):
        return self.id
    def get_pass1(self):
        return self.pass1
    def get_pass2(self):
        return self.pass2
    def set_pass1(self, password):
        self.pass1 = password
    def set_pass2(self,password):
        self.pass2 = password


