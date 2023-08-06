from __future__ import print_function
from chisubmit.tests.common import cli_test, ChisubmitCLITestCase
from chisubmit.common.utils import get_datetime_now_utc, convert_datetime_to_local,\
    set_testing_now
from chisubmit.common import CHISUBMIT_SUCCESS, CHISUBMIT_FAIL

from datetime import timedelta
import os

class CLICompleteWorkflowExtensionsPerTeam(ChisubmitCLITestCase):
        
    fixtures = ['admin_user']
        
    @cli_test
    def test_complete_with_extensions_per_team(self, runner):
        course_id = u"cmsc40200"
        course_name = u"Foobarmentals of Foobar"

        admin_id = u"admin"
        instructor_ids = [u"instructor"]
        grader_ids= [u"grader"]
        student_ids = [u"student1", u"student2", u"student3", u"student4"]
        
        all_users = instructor_ids + grader_ids + student_ids
        
        admin, instructors, graders, students = self.create_clients(runner, admin_id, instructor_ids, grader_ids, student_ids, course_id, verbose = True)
        self.create_users(admin, all_users)
        
        self.create_course(admin, course_id, course_name)

        result = admin.run("admin course set-attribute %s default_extensions 2" % (course_id))
        self.assertEqual(result.exit_code, 0)
        
        result = admin.run("admin course set-attribute %s extension_policy per-team" % (course_id))
        self.assertEqual(result.exit_code, 0)
        
        self.add_users_to_course(admin, course_id, instructors, graders, students)
        
        teams = ["student1-student2", "student3-student4"]        

        students_team = [students[0:2], students[2:4]]

        
        deadline = get_datetime_now_utc() - timedelta(hours=23)
        deadline = convert_datetime_to_local(deadline)
        deadline = deadline.replace(tzinfo=None).isoformat(sep=" ")        

        result = instructors[0].run("instructor assignment add", 
                                    ["pa1", "Programming Assignment 1", deadline])
        self.assertEqual(result.exit_code, 0)

        result = instructors[0].run("instructor assignment set-attribute", 
                                    ["pa1", "min_students", "2"])
        self.assertEqual(result.exit_code, 0)

        result = instructors[0].run("instructor assignment set-attribute", 
                                    ["pa1", "max_students", "2"])
        self.assertEqual(result.exit_code, 0)


        pa1_rubric = """Points:
    - The PA1 Tests:
        Points Possible: 50
        Points Obtained: 

    - The PA1 Design:
        Points Possible: 50
        Points Obtained: 
        
Total Points: 0 / 100
"""

        with open("pa1.rubric.txt", "w") as f:
            f.write(pa1_rubric)
            
        result = instructors[0].run("instructor assignment add-rubric", 
                                    ["pa1", "pa1.rubric.txt"])
        self.assertEqual(result.exit_code, 0)

        result = instructors[0].run("instructor assignment show-rubric", 
                                    ["pa1"])
        self.assertEqual(result.exit_code, 0)

        deadline = get_datetime_now_utc() - timedelta(hours=49)
        deadline = deadline.isoformat(sep=" ")

        result = instructors[0].run("instructor assignment add", 
                                    ["pa2", "Programming Assignment 2", deadline])
        self.assertEqual(result.exit_code, 0)

        result = instructors[0].run("instructor assignment set-attribute", 
                                    ["pa2", "min_students", "2"])
        self.assertEqual(result.exit_code, 0)

        result = instructors[0].run("instructor assignment set-attribute", 
                                    ["pa2", "max_students", "2"])
        self.assertEqual(result.exit_code, 0)

        pa2_rubric = """Points:
    - The PA2 Tests:
        Points Possible: 50
        Points Obtained: 

    - The PA2 Design:
        Points Possible: 50
        Points Obtained: 
        
Total Points: 0 / 100
"""

        with open("pa2.rubric.txt", "w") as f:
            f.write(pa2_rubric)
            
        result = instructors[0].run("instructor assignment add-rubric", 
                                    ["pa2", "pa2.rubric.txt"])
        self.assertEqual(result.exit_code, 0)
        
        result = instructors[0].run("instructor assignment show-rubric", 
                                    ["pa2"])
        self.assertEqual(result.exit_code, 0)

        result = admin.run("admin course show", ["--include-users", "--include-assignments", course_id])
        self.assertEqual(result.exit_code, 0)

        
        self.register_team(students_team[0], teams[0], "pa1", course_id)
        self.register_team(students_team[1], teams[1], "pa1", course_id)

        self.register_team(students_team[0], teams[0], "pa2", course_id)

        
        result = students_team[0][0].run("student team list")
        self.assertEqual(result.exit_code, 0)
        self.assertIn(teams[0], result.output)
        self.assertNotIn(teams[1], result.output)

        result = students_team[1][0].run("student team list")
        self.assertEqual(result.exit_code, 0)
        self.assertIn(teams[1], result.output)
        self.assertNotIn(teams[0], result.output)
        
        result = students_team[0][0].run("student team show", [teams[0]])
        self.assertEqual(result.exit_code, 0)

        result = students_team[0][0].run("student team show", [teams[1]])
        self.assertEqual(result.exit_code, CHISUBMIT_FAIL)

        result = students_team[1][0].run("student team show", [teams[1]])
        self.assertEqual(result.exit_code, 0)

        result = students_team[1][0].run("student team show", [teams[0]])
        self.assertEqual(result.exit_code, CHISUBMIT_FAIL)

        result = instructors[0].run("instructor team list")
        self.assertEqual(result.exit_code, 0)

        result = instructors[0].run("instructor team show", [teams[0]])
        self.assertEqual(result.exit_code, 0)

        result = instructors[0].run("instructor team show", [teams[1]])
        self.assertEqual(result.exit_code, 0)

        team_git_paths, team_git_repos, team_commits = self.create_team_repos(admin, course_id, teams, students_team)
        
        # Submit with just the right number
        result = students_team[0][0].run("student assignment submit", 
                                         ["pa1", "--yes"])
        self.assertEqual(result.exit_code, CHISUBMIT_SUCCESS)

        result = students_team[0][0].run("student team show", [teams[0]])
        self.assertEqual(result.exit_code, 0)

        # Try submitting an already-submitted assignment, with the same
        # commit as before (without --commit-sha)
        result = students_team[0][0].run("student assignment submit", 
                                         ["pa1", "--yes"])
        self.assertEqual(result.exit_code, CHISUBMIT_FAIL)

        # Try submitting an already-submitted assignment, with the same
        # commit as before (with --commit-sha)
        result = students_team[0][0].run("student assignment submit", 
                                         ["pa1", "--yes", "--commit-sha", team_commits[0][1].hexsha])
        self.assertEqual(result.exit_code, CHISUBMIT_FAIL)

        # Submit an already-submitted assignment
        result = students_team[0][0].run("student assignment submit", 
                                         ["pa1", "--yes", "--commit-sha", team_commits[0][0].hexsha])
        self.assertEqual(result.exit_code, CHISUBMIT_SUCCESS)
        
        result = students_team[0][0].run("student team show", [teams[0]])
        self.assertEqual(result.exit_code, 0)
        
        # Try submitting for a project the team is not registered for
        result = students_team[1][0].run("student assignment submit", 
                                         ["pa2", "--yes"])        
        self.assertEqual(result.exit_code, CHISUBMIT_FAIL)

        result = students_team[1][0].run("student assignment submit", 
                                         ["pa1", "--yes", "--commit-sha", team_commits[1][0].hexsha])
        self.assertEqual(result.exit_code, CHISUBMIT_SUCCESS)
        
        result = students_team[1][0].run("student assignment submit", 
                                         ["pa1", "--yes"])
        self.assertEqual(result.exit_code, CHISUBMIT_SUCCESS)

        result = instructors[0].run("instructor grading list-submissions", ["pa1"])
        self.assertEqual(result.exit_code, 0)

        result = instructors[0].run("instructor team pull-repos", ["repos/all/"])
        self.assertEqual(result.exit_code, 0)

        result = instructors[0].run("instructor team pull-repos", ["--assignment", "pa1", "repos/pa1/"])
        self.assertEqual(result.exit_code, 0)

        result = instructors[0].run("instructor team pull-repos", ["--assignment", "pa1", "repos/ready/", "--only-ready-for-grading"])
        self.assertEqual(result.exit_code, 0)

        # Let the deadline "pass"
        new_now = get_datetime_now_utc() + timedelta(hours=2)
        set_testing_now(new_now)

        print()
        print("~~~ Time has moved 'forward' by two hours ~~~")
        print()

        result = instructors[0].run("instructor grading list-submissions", ["pa1"])
        self.assertEqual(result.exit_code, 0)

        result = instructors[0].run("instructor team pull-repos", ["repos/all/"])
        self.assertEqual(result.exit_code, 0)

        result = instructors[0].run("instructor team pull-repos", ["--assignment", "pa1", "repos/pa1/"])
        self.assertEqual(result.exit_code, 0)

        result = instructors[0].run("instructor team pull-repos", ["--assignment", "pa1", "repos/ready/", "--only-ready-for-grading"])
        self.assertEqual(result.exit_code, 0)
                
        result = instructors[0].run("instructor grading create-grading-repos", ["--master", "pa1"])
        self.assertEqual(result.exit_code, 0)
                        
        result = instructors[0].run("instructor grading assign-graders", ["pa1"])
        self.assertEqual(result.exit_code, 0)
        
        result = instructors[0].run("instructor grading list-grader-assignments", ["pa1"])
        self.assertEqual(result.exit_code, 0)
        
        result = instructors[0].run("instructor grading push-grading", ["pa1"])
        self.assertEqual(result.exit_code, 0)
        
        result = graders[0].run("grader pull-grading", ["pa1"])
        self.assertEqual(result.exit_code, 0)
                
        team1_grading_repo_path = "chisubmit-test/repositories/%s/%s/%s" % (course_id, "pa1", teams[0])
        team2_grading_repo_path = "chisubmit-test/repositories/%s/%s/%s" % (course_id, "pa1", teams[1])
            
        team_git_repos[0], team_git_paths[0] = graders[0].get_local_git_repository(team1_grading_repo_path)
        team_git_repos[1], team_git_paths[1] = graders[0].get_local_git_repository(team2_grading_repo_path)

        
        team1_rubric_path = "%s/pa1.rubric.txt" % team_git_paths[0] 
        team2_rubric_path = "%s/pa1.rubric.txt" % team_git_paths[1] 

        team1_rubric = """Points:
    - The PA1 Tests:
        Points Possible: 50
        Points Obtained: 45

    - The PA1 Design:
        Points Possible: 50
        Points Obtained: 30
        
Penalties:
    Used O(n^156) algorithm: -10
    Submitted code in a Word document: -30

Bonuses:
    Worked alone: 15

Total Points: 50 / 100

Comments: >
    None"""

        with open(team1_rubric_path, "w") as f:
            f.write(team1_rubric)

        result = graders[0].run("grader validate-rubrics", ["pa1", "--only", teams[0]])
        self.assertEqual(result.exit_code, 0)
    
        team_git_repos[0].index.add(["pa1.rubric.txt"])
        team_git_repos[0].index.commit("Finished grading")
        
        
        
        with open("%s/bar" % team_git_paths[1], "a") as f:
            f.write("Great job!\n") 
            
        team2_rubric = """Points:
    - The PA1 Tests:
        Points Possible: 50
        Points Obtained: 50

    - The PA1 Design:
        Points Possible: 50
        Points Obtained: 45

Total Points: 95 / 100

Comments: >
    Great job!"""
                
        with open(team2_rubric_path, "w") as f:
            f.write(team2_rubric)

        result = graders[0].run("grader validate-rubrics", ["pa1", "--only", teams[1]])
        self.assertEqual(result.exit_code, 0)

        team_git_repos[1].index.add(["pa1.rubric.txt"])
        team_git_repos[1].index.add(["bar"])
        team_git_repos[1].index.commit("Finished grading")

        result = graders[0].run("grader validate-rubrics", ["pa1"])
        self.assertEqual(result.exit_code, 0)

        result = graders[0].run("grader push-grading", ["pa1"])
        self.assertEqual(result.exit_code, 0)

        result = instructors[0].run("instructor grading pull-grading", ["pa1"])
        self.assertEqual(result.exit_code, 0)
        
        result = graders[0].run("instructor grading validate-rubrics", ["pa1", "--only", teams[0]])
        self.assertEqual(result.exit_code, 0)

        result = graders[0].run("instructor grading validate-rubrics", ["pa1", "--only", teams[1]])
        self.assertEqual(result.exit_code, 0)

        result = graders[0].run("instructor grading validate-rubrics", ["pa1", "--grader", "grader"])
        self.assertEqual(result.exit_code, 0)

        result = graders[0].run("instructor grading validate-rubrics", ["pa1"])
        self.assertEqual(result.exit_code, 0)
        
        result = instructors[0].run("instructor grading show-grading-status", ["--by-grader", "pa1"])
        self.assertEqual(result.exit_code, 0)
        
        result = instructors[0].run("instructor grading collect-rubrics", ["pa1"])
        self.assertEqual(result.exit_code, 0)
        
        result = instructors[0].run("instructor grading show-grading-status", ["--use-stored-grades", "--by-grader", "pa1"])
        self.assertEqual(result.exit_code, 0)
                
        result = instructors[0].run("instructor grading list-grades")
        self.assertEqual(result.exit_code, 0)
                
        result = instructors[0].run("instructor grading push-grading", ["--to-students", "--yes", "pa1"])
        self.assertEqual(result.exit_code, 0)
        
    
        team_git_repos[0], team_git_paths[0] = students_team[0][0].get_local_git_repository(teams[0])
        team_git_repos[0].remote("origin").pull("pa1-grading:pa1-grading")
        team_git_repos[0].heads["pa1-grading"].checkout()        
        self.assertTrue(os.path.exists(team_git_paths[0] + "/pa1.rubric.txt"))

        team_git_repos[1], team_git_paths[1] = students_team[1][0].get_local_git_repository(teams[1])
        team_git_repos[1].remote("origin").pull("pa1-grading:pa1-grading")
        team_git_repos[1].heads["pa1-grading"].checkout()        
        self.assertTrue(os.path.exists(team_git_paths[0] + "/pa1.rubric.txt"))
        self.assertIn("Great job!", open(team_git_paths[1]+"/bar").read())
    
    
        