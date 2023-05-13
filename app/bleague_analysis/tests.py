from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.test import TestCase, Client, RequestFactory

from bleague_analysis.views import top
from bleague_analysis.models import Team


# Create your tests here.

UserModel = get_user_model()

class TopPageViewTest(TestCase):
    def test_top_page_returns_200_and_expected_title(self):
        response = self.client.get('/')
        self.assertContains(response, 'Bリーグ分析サイト', status_code=200)

    def test_top_page_uses_expected_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'bleague_analysis/top.html')

class TopPageRenderBleagueTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username='test_user',
            email='test@example.com',
            password='passward'
        )
        self.team = Team.objects.create(
            title = 'title1',
        )
        
    def test_should_return_team_name(self):
        request = RequestFactory().get('/')
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.user.username)



class TeamDetailTest(TestCase):
    def test_should_use_expected_template(self):
        response = self.client.get("/teams/%s/" % self.team.bleague_id)
        self.assertTemplateUsed(response, "bleague_analysis/team_detail.html")

    def test_top_page_200_and_expected_heading(self):
        response = self.client.get("/teams/%s/" % self.team.bleague_id)
        self.assertContains(response, "bleague_analysis/team_detail.html", status_code=200)