from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    """news表单"""
    title = StringField(label="新闻标题", validators=[DataRequired()],
                        description="请输入标题",
                        render_kw={"required":"required"})
    content = TextAreaField(label="新闻内容",
                            render_kw={"required":"required"}
                            )
    types = SelectField("新闻类型", choices=[('1',"推荐"), ('2',"本地")])
    images = StringField(label="新闻图片", render_kw={"required":"required"})
    submit = SubmitField("提交")
