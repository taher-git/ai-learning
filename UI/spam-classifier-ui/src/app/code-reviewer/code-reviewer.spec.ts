import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CodeReviewer } from './code-reviewer';

describe('CodeReviewer', () => {
  let component: CodeReviewer;
  let fixture: ComponentFixture<CodeReviewer>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CodeReviewer]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CodeReviewer);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
