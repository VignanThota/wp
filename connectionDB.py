from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, join
import datetime
from sqlalchemy import Column, Integer, String ,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import session
engine=create_engine('sqlite:///blog.db', echo=False)
Base=declarative_base()
class Blog_Posts(Base):
    __tablename__='blog_Posts'
        # PRIMARY KEY (id)
    Id = Column(Integer,primary_key=True)
    Title=Column(String)
    Message=Column(String,)
    Date = DateTime(default=datetime.datetime.utcnow)
    # Date = Column(DateTime, default=datetime.datetime.utcnow)
    def __repr__(self):
        return "<UserDetails(Id='%s', Title='%s', Message='%s'>" %(self.Id,self.Title,self.Message)
Base.metadata.create_all(engine)
Session=sessionmaker(bind=engine)
session=Session()
def addPost(title,message):
    print(title)
    print(message)
    print("12345678")
    new_post=Blog_Posts(Title=title,Message=message,Date=Date)
    session.add(new_post)
    session.commit()
    return "successfully"
# def viewposts():
# 	print("success")
# 	output = "<html><body>List Of Users SignedIn<br>"
# 	posts = session.query(Blog_Posts).all()
# 	output += "<html><body>List Of Users SignedIn<br>"
# 	for i in posts:
# 		output += i.Title
# 		output += i.Message
# 		output += "</br>"
# 		output += "</br></br></br>"
# 		print(i.Title)
# 	output += "</body></html>"
# 	# # self.wfile.write(output.encode())
# 	return